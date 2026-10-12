"""
Parameterized SQL Query Builder for Caption History
"""

class QueryBuilder:
    @staticmethod
    def build(style: str = None, search: str = None, limit: int = 50, offset: int = 0):
        clauses = []
        params = []
        if style:
            clauses.append("style = ?")
            params.append(style)
        if search:
            clauses.append("(caption_text LIKE ? OR image_name LIKE ?)")
            params.extend([f"%{search}%", f"%{search}%"])

        where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
        sql = f"SELECT * FROM captions {where_sql} ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        return sql, tuple(params)
