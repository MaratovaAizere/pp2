import psycopg2

# ---------- CONNECTION ----------
# Adjust credentials to match your local PostgreSQL setup.
_conn = psycopg2.connect(
    dbname="snake_db",
    user="postgres",
    password="24680",
    host="localhost",
)
_conn.autocommit = True
_cur = _conn.cursor()


# ---------- SCHEMA ----------
def create_tables() -> None:
    _cur.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id       SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL
    );
    """)

    _cur.execute("""
    CREATE TABLE IF NOT EXISTS game_sessions (
        id            SERIAL PRIMARY KEY,
        player_id     INTEGER REFERENCES players(id),
        score         INTEGER   NOT NULL,
        level_reached INTEGER   NOT NULL,
        played_at     TIMESTAMP DEFAULT NOW()
    );
    """)


# ---------- PLAYERS ----------
def get_or_create_player(username: str) -> int:
    """Return the player id, creating a new row if needed."""
    _cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    row = _cur.fetchone()
    if row:
        return row[0]

    _cur.execute(
        "INSERT INTO players (username) VALUES (%s) RETURNING id",
        (username,),
    )
    return _cur.fetchone()[0]


# ---------- SESSIONS ----------
def save_game(player_id: int, score: int, level: int) -> None:
    _cur.execute(
        """
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
        """,
        (player_id, score, level),
    )


def get_top_scores(limit: int = 10) -> list[tuple]:
    """Return [(username, score, level_reached, played_at), ...]
    One row per player — their personal best session only.
    """
    _cur.execute(
        """
        SELECT DISTINCT ON (g.player_id)
               p.username,
               g.score,
               g.level_reached,
               TO_CHAR(g.played_at, 'YYYY-MM-DD') AS day
        FROM   game_sessions g
        JOIN   players p ON g.player_id = p.id
        ORDER  BY g.player_id, g.score DESC
        """,
    )
    rows = _cur.fetchall()
    # sort all best-per-player rows by score and take top N
    rows.sort(key=lambda r: r[1], reverse=True)
    return rows[:limit]


def get_best_score(player_id: int) -> int:
    _cur.execute(
        "SELECT MAX(score) FROM game_sessions WHERE player_id = %s",
        (player_id,),
    )
    res = _cur.fetchone()[0]
    return res if res else 0