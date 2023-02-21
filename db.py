import pymysql
import sqlalchemy
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from sqlalchemy.dialects import mysql

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = 'sqlite:///db.sqlite'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    user_tg_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    balance = sqlalchemy.Column(sqlalchemy.Integer)
    podpiska = sqlalchemy.Column(sqlalchemy.VARCHAR(20))  # выполнял задание дня = True, нет = False
    end_pod = sqlalchemy.Column(sqlalchemy.VARCHAR(20))  # Дата оканчания подписки
    pol = sqlalchemy.Column(sqlalchemy.VARCHAR(20))  # woman or man
    state = sqlalchemy.Column(sqlalchemy.VARCHAR(20))
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(200))
    phone_number = sqlalchemy.Column(sqlalchemy.VARCHAR(200))
    zar_today = sqlalchemy.Column(sqlalchemy.Integer)  # Заработал сегодня
    zar_mesyaz = sqlalchemy.Column(sqlalchemy.Integer)  # Заработал в этом месяц
    partner_phone_number = sqlalchemy.Column(sqlalchemy.VARCHAR(200))
    start_date_every_day = sqlalchemy.Column(sqlalchemy.VARCHAR(200),
                                             default="01.01.1980")  # Начало получение награждений за сис.еври дэй
    buy_all = sqlalchemy.Column(sqlalchemy.VARCHAR(2),default="N") #N = no, Y = yes
    count_day_every_day = sqlalchemy.Column(sqlalchemy.Integer)  # сколько дней получал ежедневную награду
    last_date_taked_every_day = sqlalchemy.Column(sqlalchemy.VARCHAR(200),
                                                  default="01.01.1980")  # Последний день когда получал ежедневную награду
    take_pose = sqlalchemy.Column(sqlalchemy.VARCHAR(20))  # False не брал и True если брал
    need_promocode_price = sqlalchemy.Column(sqlalchemy.VARCHAR(20),
                                             nullable=True)  # цена необходимого промокода, если None то он не нужен
    partner_name = sqlalchemy.Column(sqlalchemy.VARCHAR(200), default="партнёр")


class Promocode(SqlAlchemyBase):
    __tablename__ = 'promocodes'
    code = sqlalchemy.Column(sqlalchemy.VARCHAR(100), primary_key=True)  # промокод
    value = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)  # скидка
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)  # цена
    minimum_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)  # минимальная стоимость заказа
    end_date = sqlalchemy.Column(sqlalchemy.VARCHAR(40), nullable=False)  # действует до этой даты
    user_tg_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)  # tg_id


class Open_poses(SqlAlchemyBase):
    __tablename__ = 'open_poses'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    pos_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    pos_level = sqlalchemy.Column(sqlalchemy.BigInteger)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    user_id = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    see = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))  # True смотрел и False не смотрел


class Present(SqlAlchemyBase):
    __tablename__ = 'present'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    present_id = sqlalchemy.Column(sqlalchemy.BigInteger)  # 1 это самый первый подарок
    used = sqlalchemy.Column(sqlalchemy.VARCHAR(20))  # False это не юзанный, True это юзанный


class Poses(SqlAlchemyBase):
    __tablename__ = 'poses'
    pos_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    pos_lvl = sqlalchemy.Column(sqlalchemy.BigInteger)
    photo_base_64 = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    file_id = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))


class Order(SqlAlchemyBase):
    __tablename__ = 'orders'
    order_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)  # id заказа
    coins = sqlalchemy.Column(sqlalchemy.BigInteger)  # количество выдаваемых монет
    user_tg_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)  # tg id пользователя


class Free_game(SqlAlchemyBase):
    __tablename__ = 'free_game'
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    game_name = sqlalchemy.Column(sqlalchemy.VARCHAR(200))
    game_caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))


class Paid_game(SqlAlchemyBase):
    __tablename__ = 'paid_game'
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    game_name = sqlalchemy.Column(sqlalchemy.VARCHAR(200))
    game_caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    detail = sqlalchemy.Column(sqlalchemy.VARCHAR(600))


class Purchased_game(SqlAlchemyBase):
    __tablename__ = 'purchased_game'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    user_id = sqlalchemy.Column(sqlalchemy.BigInteger)


class Paid_game_info_1(SqlAlchemyBase):
    __tablename__ = 'paid_game_info_1'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    dop_info = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824), nullable=True)


class Progress(SqlAlchemyBase):
    __tablename__ = 'progress'
    id = sqlalchemy.Column(sqlalchemy.Integer, autoincrement=True, primary_key=True)
    user_tg_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    gam_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    lvl = sqlalchemy.Column(sqlalchemy.BigInteger)
    dop_info = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)


class For_paid_game_info_1(SqlAlchemyBase):
    __tablename__ = 'for_paid_game_info_1'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    players = sqlalchemy.Column(sqlalchemy.BigInteger)  # Количество игроков
    play_now = sqlalchemy.Column(sqlalchemy.BigInteger)  # Сейчас в игре
    player1_id = sqlalchemy.Column(sqlalchemy.BigInteger)  # tg_id первого
    player2_id = sqlalchemy.Column(sqlalchemy.BigInteger)  # tg_id второго
    player1_count = sqlalchemy.Column(sqlalchemy.BigInteger)  # очки первого
    player2_count = sqlalchemy.Column(sqlalchemy.BigInteger)  # очки второго
    play = sqlalchemy.Column(sqlalchemy.BigInteger)  # 1 играем, 0 не играем
    wish1 = sqlalchemy.Column(sqlalchemy.VARCHAR(2000))  # желание первого
    wish2 = sqlalchemy.Column(sqlalchemy.VARCHAR(2000))  # желание второго
    vop1 = sqlalchemy.Column(sqlalchemy.VARCHAR(2000))
    vop2 = sqlalchemy.Column(sqlalchemy.VARCHAR(2000))
    game_id_id = sqlalchemy.Column(sqlalchemy.BigInteger)  # id игры в игре


class For_paid_game_info_2(SqlAlchemyBase):
    __tablename__ = 'for_paid_game_info_2'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    player1_id = sqlalchemy.Column(sqlalchemy.BigInteger)  # tg_id первого
    player2_id = sqlalchemy.Column(sqlalchemy.BigInteger)  # tg_id второго
    hwo_last = sqlalchemy.Column(sqlalchemy.BigInteger)  # кто играл последний
    play = sqlalchemy.Column(sqlalchemy.BigInteger)  # 1 играем, 0 не играем
    player1_count = sqlalchemy.Column(sqlalchemy.BigInteger)
    player2_count = sqlalchemy.Column(sqlalchemy.BigInteger)


class For_paid_game_info_6(SqlAlchemyBase):  # будет хранится инфа по 6 игре, все игры сделаны или нет
    __tablename__ = 'for_paid_game_info_6'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    id_from_game = sqlalchemy.Column(sqlalchemy.BigInteger)
    user_tg_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    name = sqlalchemy.Column(sqlalchemy.BigInteger)
    do = sqlalchemy.Column(sqlalchemy.VARCHAR)  # Сделано или нет

class For_paid_game_info_9(SqlAlchemyBase):  # будет хранится инфа по 6 игре, все игры сделаны или нет
    __tablename__ = 'for_paid_game_info_9'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    pose_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    discrip = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))

class Paid_game_info_2(SqlAlchemyBase):
    __tablename__ = 'paid_game_info_2'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    dop_info = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824), nullable=True)


class Paid_game_info_3(SqlAlchemyBase):
    __tablename__ = 'paid_game_info_3'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    dop_info = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824), nullable=True)


class Paid_game_info_4(SqlAlchemyBase):
    __tablename__ = 'paid_game_info_4'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    dop_info = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824), nullable=True)


class Paid_game_info_5(SqlAlchemyBase):
    __tablename__ = 'paid_game_info_5'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    dop_info = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824), nullable=True)


class Paid_game_info_6(SqlAlchemyBase):
    __tablename__ = 'paid_game_info_6'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    dop_info = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824), nullable=True)


class Paid_game_info_7(SqlAlchemyBase):
    __tablename__ = 'paid_game_info_7'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    dop_info = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824), nullable=True)


class Paid_game_info_8(SqlAlchemyBase):
    __tablename__ = 'paid_game_info_8'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    dop_info = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824), nullable=True)


class Paid_game_info_9(SqlAlchemyBase):
    __tablename__ = 'paid_game_info_9'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    dop_info = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824), nullable=True)


class Paid_game_info_11(SqlAlchemyBase):
    __tablename__ = 'paid_game_info_11'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    dop_info = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824), nullable=True)


class Paid_game_info_10(SqlAlchemyBase):
    __tablename__ = 'paid_game_info_10'
    id = sqlalchemy.Column(sqlalchemy.INTEGER, autoincrement=True, primary_key=True)
    game_id = sqlalchemy.Column(sqlalchemy.BigInteger)
    caption = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824))
    dop_info = sqlalchemy.Column(sqlalchemy.VARCHAR(1073741824), nullable=True)
