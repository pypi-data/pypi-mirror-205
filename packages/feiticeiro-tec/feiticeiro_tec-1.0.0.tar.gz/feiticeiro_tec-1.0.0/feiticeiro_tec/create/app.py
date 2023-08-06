from server import Servidor
from loguru import logger
from dotenv import load_dotenv

load_dotenv('.env')

logger.add(
    'logs/server.log',
    rotation='1 day',
    retention='7 days',
    level='DEBUG'
)

app = Servidor()
app.init_database()
app.init_api()
app.init_commands()


if __name__ == '__main__':
    app.run()
