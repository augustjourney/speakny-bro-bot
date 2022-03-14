from fastapi_sqlalchemy import db

import json
class UsersRepo:
    def get_user(chat_id):
        query = """
            SELECT chat_id, first_name, language_code, settings
            FROM speaknybro_user
            WHERE chat_id = :chat_id; 
        """
        try:
            with db():
                user = db.session.execute(query, { 'chat_id':chat_id }).first()
                if user:
                    return {                    
                        'chat_id': user[0],
                        'first_name': user[1],
                        'language_code': user[2],
                        'settings':user[3],
                    }
                return None
        except Exception as e:
            print(e)

    def update_user_settings(chat_id, settings):
        query = """
            UPDATE speaknybro_user
            SET settings = :settings
            WHERE chat_id = :chat_id
            RETURNING chat_id, first_name, language_code, settings; 
        """
        try:
            with db():
                props = { 'chat_id': chat_id, 'settings': json.dumps(settings) }
                db.session.execute(query, props).first()          
                return db.session.commit()
        except Exception as e:
            print(e)

    def create_user(chat_id, username, first_name, language_code, settings):
        query = """
            INSERT INTO speaknybro_user
            (chat_id, username, first_name, language_code, is_active, settings)
            VALUES (:chat_id, :username, :first_name, :language_code, True, :settings)
            RETURNING chat_id, first_name, language_code, settings; 
        """
        try:
            with db():
                props = { 
                    'chat_id': chat_id, 
                    'username': username, 
                    'first_name': first_name, 
                    'language_code': language_code, 
                    'settings': json.dumps(settings) 
                }
                db.session.execute(query, props).first()
                db.session.commit()            
                return {
                    'chat_id': chat_id,
                    'first_name': first_name,
                    'language_code': language_code,
                    'settings':settings,
                }
        except Exception as e:
            print(e)