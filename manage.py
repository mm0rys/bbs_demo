from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from bbs_demo import app
from exts import db

db.init_app(app)
manager =Manager(app)

# Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到Command
manager.add_command('db', MigrateCommand)

if __name__ =="__main__":
    manager.run()