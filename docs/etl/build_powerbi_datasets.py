import os
import json
import pandas as pd
import mysql.connector
from datetime import datetime

RAW_DIR = "raw_json"

FILES = {
    "token_overview": "v2_token_overview.json",
    "token": "v2_token.json",
    "twitter": "v4_x_tweets.json",
    "reddit": "v5_reddit_post_engagement.json"
}

def log(msg):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Japgun@2014",
        database="noodles_dw"
    )

# ---------------- LOAD JSON ----------------

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return pd.DataFrame(data)
    if isinstance(data, dict):
        return pd.json_normalize(data)
    return pd.DataFrame()

# ---------------- UPSERT DIMCURRENCY ----------------

def upsert_dimcurrency(conn, df):
    cursor = conn.cursor()

    for _, row in df.iterrows():
        symbol = row.get("symbol") or row.get("token_symbol")
        name = row.get("name") or row.get("token_name")

        if not symbol:
            continue

        cursor.execute("""
            INSERT INTO dimcurrency (Symbol, CurrencyName, LoadDate)
            VALUES (%s, %s, NOW())
            ON DUPLICATE KEY UPDATE CurrencyName = VALUES(CurrencyName)
        """, (symbol, name))

    conn.commit()
    cursor.close()
    log("DimCurrency updated.")

# ---------------- UPSERT DIMPLATFORM ----------------

def upsert_dimplatform(conn):
    cursor = conn.cursor()
    platforms = [("Twitter",), ("Reddit",)]

    cursor.executemany("""
        INSERT INTO dimplatform (PlatformName)
        VALUES (%s)
        ON DUPLICATE KEY UPDATE PlatformName = VALUES(PlatformName)
    """, platforms)

    conn.commit()
    cursor.close()
    log("DimPlatform updated.")

# ---------------- UPSERT DIMDATE ----------------

def upsert_dimdate(conn, dates):
    cursor = conn.cursor()

    for d in dates:
        if isinstance(d, str):
            try:
                d = datetime.strptime(d[:10], "%Y-%m-%d").date()
            except:
                continue

        date_key = int(d.strftime("%Y%m%d"))  # <-- FIXED

        cursor.execute("""
            INSERT INTO dimdate (
                DateKey, FullDate, Year, Quarter, Month, MonthName,
                Week, DayOfMonth, DayOfWeek, DayName, IsWeekend
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE FullDate = VALUES(FullDate)
        """, (
            date_key,
            d,
            d.year,
            (d.month - 1)//3 + 1,
            d.month,
            d.strftime("%B"),
            d.isocalendar().week,
            d.day,
            d.isoweekday(),
            d.strftime("%A"),
            1 if d.isoweekday() >= 6 else 0
        ))

    conn.commit()
    cursor.close()


# ---------------- FACT SOCIAL ENGAGEMENT ----------------

def get_dim_ids(conn, symbol, platform, date):
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT CurrencyKey FROM dimcurrency WHERE Symbol=%s", (symbol,))
    c = cursor.fetchone()
    currency_id = c["CurrencyKey"] if c else None

    cursor.execute("SELECT PlatformID FROM dimplatform WHERE PlatformName=%s", (platform,))
    p = cursor.fetchone()
    platform_id = p["PlatformID"] if p else None

    cursor.execute("SELECT DateKey FROM dimdate WHERE FullDate=%s", (date,))
    d = cursor.fetchone()
    date_id = d["DateKey"] if d else None

    cursor.close()
    return currency_id, platform_id, date_id

def load_twitter(conn, df):
    cursor = conn.cursor()

    for _, row in df.iterrows():
        symbol = row.get("symbol") or row.get("token_symbol")
        if not symbol:
            continue

        created = row.get("created_at")
        if not created:
            continue

        try:
            dt = datetime.fromisoformat(created.replace("Z", ""))
        except:
            dt = datetime.strptime(created[:10], "%Y-%m-%d")

        date = dt.date()

        like_count = int(row.get("like_count", 0))
        reply_count = int(row.get("reply_count", 0))
        retweet_count = int(row.get("retweet_count", 0))
        quote_count = int(row.get("quote_count", 0))

        engagement = like_count + reply_count + retweet_count + quote_count
        post_id = row.get("id") or row.get("tweet_id")

        currency_id, platform_id, date_id = get_dim_ids(conn, symbol, "Twitter", date)
        if not (currency_id and platform_id and date_id):
            continue

        cursor.execute("""
            INSERT INTO factsocialengagement (
                CurrencyID, PlatformID, DateID, PlatformPostID,
                LikeCount, ReplyCount, RetweetCount, QuoteCount, EngagementScore
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            currency_id, platform_id, date_id, str(post_id),
            like_count, reply_count, retweet_count, quote_count, engagement
        ))

    conn.commit()
    cursor.close()
    log("Twitter → FactSocialEngagement loaded.")

def load_reddit(conn, df):
    cursor = conn.cursor()

    for _, row in df.iterrows():
        symbol = row.get("symbol") or row.get("token_symbol")
        if not symbol:
            continue

        created = row.get("created_utc")
        if not created:
            continue

        try:
            dt = datetime.fromisoformat(str(created).replace("Z", ""))
        except:
            dt = datetime.strptime(str(created)[:10], "%Y-%m-%d")

        date = dt.date()

        upvotes = int(row.get("upvotes", row.get("score", 0)))
        comments = int(row.get("comments", row.get("num_comments", 0)))
        engagement = upvotes + comments

        post_id = row.get("id") or row.get("post_id")

        currency_id, platform_id, date_id = get_dim_ids(conn, symbol, "Reddit", date)
        if not (currency_id and platform_id and date_id):
            continue

        cursor.execute("""
            INSERT INTO factsocialengagement (
                CurrencyID, PlatformID, DateID, PlatformPostID,
                LikeCount, ReplyCount, RetweetCount, QuoteCount, EngagementScore
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            currency_id, platform_id, date_id, str(post_id),
            upvotes, comments, 0, 0, engagement
        ))

    conn.commit()
    cursor.close()
    log("Reddit → FactSocialEngagement loaded.")

# ---------------- MAIN ----------------

def main():
    log("Starting ETL...")

    conn = get_connection()

    df_token_overview = load_json(os.path.join(RAW_DIR, FILES["token_overview"]))
    df_token = load_json(os.path.join(RAW_DIR, FILES["token"]))
    df_twitter = load_json(os.path.join(RAW_DIR, FILES["twitter"]))
    df_reddit = load_json(os.path.join(RAW_DIR, FILES["reddit"]))

    df_tokens = df_token if not df_token.empty else df_token_overview

    upsert_dimcurrency(conn, df_tokens)
    upsert_dimplatform(conn)

    all_dates = set()

    for _, r in df_twitter.iterrows():
        if r.get("created_at"):
            all_dates.add(r["created_at"][:10])

    for _, r in df_reddit.iterrows():
        if r.get("created_utc"):
            all_dates.add(str(r["created_utc"])[:10])

    upsert_dimdate(conn, all_dates)

    load_twitter(conn, df_twitter)
    load_reddit(conn, df_reddit)

    conn.close()
    log("ETL complete.")

if __name__ == "__main__":
    main()
