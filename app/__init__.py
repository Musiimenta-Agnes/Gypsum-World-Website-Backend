
from flask import Flask, send_from_directory
from app.extensions import db, migrate, bcrypt, jwt
from flask_cors import CORS
from flask_mail import Mail
import os
from datetime import timedelta

# Initialize mail extension outside create_app so it can be imported
mail = Mail()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "http://www.okuosigypsum.com"}}, supports_credentials=True)
    app.config.from_object('config.Config')

    # Upload config
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    # Your existing secret keys and JWT config
    app.config['SECRET_KEY'] = 'super-secret-key'
    app.config['JWT_SECRET_KEY'] = 'super-secret-jwt-key'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=60)

    # *** Add your mail configuration here ***
    app.config['MAIL_DEFAULT_SENDER'] = 'musiimentaagnes9@gmail.com'  # or whatever email you want as sender

    app.config['MAIL_SERVER'] = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('SMTP_PORT', 587))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('SMTP_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('SMTP_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('SMTP_USERNAME')  


    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, supports_credentials=True)
    mail.init_app(app)  # Initialize Flask-Mail

    # Import your models and blueprints here as you already do

    from app.controllers.user.user_controller import user_bp
    from app.controllers.product.product_controller import product_bp
    from app.controllers.order.place_order_controller import place_order_bp
    from app.controllers.direct_order_message.direct_order_sms import direct_order_bp
    from app.controllers.dashboard.dashboard_controller import dashboard_bp
    from app.controllers.page_viwers.page_viewers_controller import view_bp
    from app.controllers.user_otp.user_otp_controller import otp_bp
    # from app.controllers.order.analytics import analytics_bp
    from app.controllers.contact_info.contact_info_controller import contact_bp
    from app.controllers.about.about_controller import about_bp
    from app.controllers.freq_asked_qns.questions_controller import questions_bp
    from app.controllers.project_controller import project_bp
    from app.controllers.gallery_controller import gallery_bp
    from app.controllers.material_controller import material_bp

    # Models
    from app.models.order.order_model import Order
    from app.models.order_item.order_item_model import OrderItem
    from app.models.product.product_model import Product
    from app.models.user.user_model import User
    from app.models.cart.cart_item_model import CartItem
    from app.models.user_otp.user_otp_model import UserOTP
    from app.models.direct_order_message.direct_order import DirectMessage
    from app.models.page_views.page_viewers_model import PageView
    from app.models.monthly_sales.monthly_sales import MonthlySalesPerformance
    from app.models.contact_info.contact_info_model import ContactInfo
    from app.models.about.about_model import AboutContent
    from app.models.freq_asked_qns.questions_model import FAQ
    from app.models.project_model import Project
    from app.models.gallery_model import Gallery
    from app.models.material_model import Material

    app.register_blueprint(user_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(place_order_bp)
    app.register_blueprint(direct_order_bp)
    app.register_blueprint(view_bp)
    app.register_blueprint(otp_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(questions_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(material_bp)

    @app.route('/static/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(os.path.join(app.root_path, 'static', 'uploads'), filename)

    @app.route("/")
    def welcome_page():
        return """
        <div style="font-family: Arial, sans-serif; padding: 40px; text-align: center;">
            <h1 style="color: #1F3C88;">Gypsum World & Building Construction Materials</h1>
            <p style="color: #555;">Official API & Backend Management System</p>
            <p><strong>Partitions:</strong> Gypsum Construction | Building & Plumbing Materials</p>
            <p><strong>Senior Manager:</strong> Agnes | <strong>Viewer:</strong> Banx</p>
        </div>
        """



    return app

