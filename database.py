import sqlite3 as sql
import bcrypt

class Database:
   
   def __init__(self):
       self.create_table()
       

   def create_table(self):
      self.connect=sql.connect("Accounts_Information.db")
      self.cursor=self.connect.cursor()
      self.cursor.execute("CREATE TABLE IF NOT EXISTS mail_accounts(id INTEGER PRIMARY KEY, mail_Address TEXT NOT NULL UNIQUE, password TEXT NOT NULL)")
      self.connect.commit()
      self.connect.close()

   def add_account(self,account_mail, account_password):
        try:
            self.connect = sql.connect("Accounts_Information.db")
            self.cursor = self.connect.cursor()
            self.cursor.execute("INSERT INTO mail_accounts (mail_Address, password) VALUES(?,?)",(account_mail, account_password))
            self.connect.commit()
            self.connect.close()
        except sql.IntegrityError as e:
           return f"error: {e}"
        except Exception as e:
           return f"error: {e}"
        return "added"

   def update_account(self,account_mail,account_password,new_account_mail=None,new_account_password=None):

        try:
            self.connect=sql.connect("Accounts_Information.db")
            self.cursor=self.connect.cursor()

            if new_account_mail and new_account_password:
                self.cursor.execute("SELECT password FROM mail_accounts WHERE mail_Address=?",(account_mail,))

                my_result=self.cursor.fetchone()

                if my_result is None:
                    return "Not found"

                if not bcrypt.checkpw(account_password.encode(),my_result[0].encode()):
                    return "sorry"

                my_hashed_password=my_hashed_password=bcrypt.hashpw(new_account_password.encode(),bcrypt.gensalt()).decode()

                self.cursor.execute("UPDATE mail_accounts SET mail_Address=?, password=? WHERE mail_Address=?",(new_account_mail,my_hashed_password,account_mail))
                self.connect.commit()
                return "Email and password have been updated"
            
            elif new_account_password:
                self.cursor.execute("SELECT password FROM mail_accounts WHERE mail_Address=?",(account_mail,))

                my_result=self.cursor.fetchone()

                if my_result is None:
                    return "not found"

                if not bcrypt.checkpw(account_password.encode(),my_result[0].encode()):
                    return "Wrong password"

                my_hashed_password=bcrypt.hashpw(new_account_password.encode(),bcrypt.gensalt()).decode()

                self.cursor.execute("UPDATE mail_accounts SET password=? WHERE mail_Address=?",(my_hashed_password,account_mail))

                self.connect.commit()
                return "Password updated"
            
            elif new_account_mail:
                self.cursor.execute("SELECT password FROM mail_accounts WHERE mail_Address=?",(account_mail,))
                my_result = self.cursor.fetchone()

                if my_result is None:
                    return "Not found"

                if not bcrypt.checkpw(account_password.encode(),my_result[0].encode()):
                    return "Sorry"

                self.cursor.execute("UPDATE mail_accounts SET mail_Address=? WHERE mail_Address=?",(new_account_mail,account_mail))
                self.connect.commit()
                
                return "Email address updated"
        
            return "No changes have been made"

        except sql.IntegrityError as e:
           return f"{e}"

        except Exception as e:
            return f"{e}"
    
        finally:
           self.connect.close()

   def delete_account(self,account_mail,account_password):

        try:
            self.connect=sql.connect("Accounts_Information.db")
            self.cursor=self.connect.cursor()
            self.cursor.execute("SELECT password FROM mail_accounts WHERE mail_Address=?",(account_mail,))

            my_result=self.cursor.fetchone()

            if my_result is None:
                return "No account found to delete"

            if not bcrypt.checkpw(account_password.encode(),my_result[0].encode()):
                return "Sorry"

            self.cursor.execute("DELETE FROM mail_accounts WHERE mail_Address=?",(account_mail,))
        
            self.connect.commit()

            return "Account deleted"

        except Exception as e:
            return f"{e}"

        finally:
            self.connect.close()

    

   def show_users_information(self,mail,password):

        try:
            self.connect=sql.connect("Accounts_Information.db")
            self.cursor=self.connect.cursor()
            self.cursor.execute("SELECT * FROM mail_accounts WHERE mail_Address=?",(mail,))
            find_Accounts=self.cursor.fetchone()
            

            if find_Accounts is None:
                return f"Email address: {mail} and password: {password} were not found"

            my_stored_hash=find_Accounts[2]
           
            if bcrypt.checkpw(password.encode("utf-8"),my_stored_hash.encode("utf-8")):
                return f"Email address : {find_Accounts[1]} , password : {find_Accounts[2]} were found "
            else:
                print("Sorry")

        except Exception as e:
            return f"error:{e}"

        finally:
            self.connect.close()
        
    
    
    

    


    

