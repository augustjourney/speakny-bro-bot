from fastapi_sqlalchemy import db

class SpeechRepo:
    def create_speech(text, native, language, chat_id):
        query = """
            WITH sp_user AS (
                SELECT * FROM speaknybro_user
                WHERE chat_id = :chat_id
                LIMIT 1
            )
            INSERT INTO speaknybro_speech
            (text, native, language, user_id)
            VALUES (:text, :native, :language, 
                (SELECT sp_user.id AS user_id FROM sp_user)
            )
            RETURNING id; 
        """
        try:
            with db():
                props = { 
                    'text': text, 
                    'native': native, 
                    'language': language, 
                    'chat_id': chat_id 
                }
                db.session.execute(query, props).first()          
                return db.session.commit()
        except Exception as e:
            print(e)