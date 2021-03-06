import logging
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """
    def __init__(self, statement):
        print statement

class Item(db.Model):
    """ Model for an Item """
    logger = logging.getLogger(__name__)
    app = None

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Item %r>' % (self.name)

    def save(self):
        """ Saves an Item to the database """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Deletes an Item from the database """
        if self.id:
            db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """
        Serializes an Item into a dictionary

        Returns:
            dict
        """
        return {
                "id": self.id,
                "order_id": self.order_id,
                "product_id": self.product_id,
                "name": self.name,
                "quantity": self.quantity,
                "price": self.price
                }

    def deserialize(self, data, order_id):
        """
        Deserializes an Item from a dictionary

        Args:
            data (dict): A dictionary containing the Item data

        Returns:
            self: instance of Item

        Raises:
            DataValidationError: when bad or missing data
        """
        try:
            self.order_id = order_id
            self.product_id = data['product_id']
            self.name = data['name']
            self.quantity = data['quantity']
            self.price = data['price']
        except KeyError as error:
            raise DataValidationError('Invalid item: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid item: body of request contained ' \
                                      'bad or no data')
        return self

    @staticmethod
    def init_db(app):
        """ Initializes the database session """
        Item.logger.info('Initializing database')
        Item.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @staticmethod
    def all():
        """
        Fetch all of the Items in the database

        Returns:
            List: list of Items
        """
        Item.logger.info('Processing all Items')
        return Item.query.all()

    @staticmethod
    def get(item_id):
        """
        Get an Item by id

        Args:
            item_id: primary key of items

        Returns:
            Item: item with associated id
        """
        Item.logger.info('Processing lookup for id %s ...', item_id)
        return Item.query.get(item_id)


class Order(db.Model):
    """ Model for an Item """
    logger = logging.getLogger(__name__)
    app = None

    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    shipped = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Order>'

    def save(self):
        """ Saves an Order to the database """
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Deletes an Order from the database """
        if self.id:
            db.session.delete(self)
        db.session.commit()

    def serialize(self):
        """
        Serializes an Order into a dictionary

        Returns:
            dict
        """
        return {
                "id": self.id,
                "customer_id": self.customer_id,
                "date": self.date,
                "shipped": self.shipped
                }

    def deserialize(self, data):
        """
        Deserializes an Order from a dictionary

        Args:
            data (dict): A dictionary containing the Order data

        Returns:
            self: instance of Order

        Raises:
            DataValidationError: when bad or missing data
        """
        try:
            self.customer_id = data['customer_id']
            self.date = datetime.strptime(data['date'], "%Y-%m-%d %H:%M:%S.%f")
            self.shipped = data['shipped']
        except KeyError as error:
            raise DataValidationError('Invalid order: missing ' + error.args[0])
        except TypeError as error:
            raise DataValidationError('Invalid order: body of request contained ' \
                                      'bad or no data')
        return self

    @staticmethod
    def init_db(app):
        """ Initializes the database session """
        Order.logger.info('Initializing database')
        Order.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @staticmethod
    def all():
        """
        Fetch all of the Orders in the database

        Returns:
            List: list of Orders
        """
        Order.logger.info('Processing all Orders')
        return Order.query.all()

    @staticmethod
    def get(order_id):
        """
        Get an Order by id

        Args:
            order_id: primary key of orders

        Returns:
            Order: order with associated id
        """
        Order.logger.info('Processing lookup for id %s ...', order_id)
        return Order.query.get(order_id)

    @staticmethod
    def find_by_customer_id(customer_id):
        """ Returns all Orders placed by the given customer

        Args:
            customer_id (integer): the customer's id
        """
        Order.logger.info('Processing customer_id query for %s ...', customer_id)
        return Order.query.filter(Order.customer_id == customer_id)
