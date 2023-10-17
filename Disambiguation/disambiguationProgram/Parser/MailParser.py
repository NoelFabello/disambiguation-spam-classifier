from Parser.Parser import Parser
import email
from email import policy
import traceback
class MailParser(Parser):
    #Obtención del cuerpo del correo electrónico
    def parse(self, file):
        message = ''
        with open(file, 'rb') as f:
            try:
                msg = email.message_from_binary_file(f, policy=policy.default)
            except Exception as e:
                print(e.with_traceback())
            content = msg.get_payload(decode=True)
            try:
                message = content.decode('UTF-8')
            except UnicodeDecodeError:
                try:
                    message = content.decode('ISO-8859-1')
                except UnicodeDecodeError:
                    print("Unicode Error en file: ", file)
                    traceback.print_exc()
            except Exception as e:
                print("Error during parse from:", file)
                traceback.print_exc()
        return message
