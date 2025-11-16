from flask import Flask, render_template, redirect, url_for


def create_app():
    app = Flask(
        __name__,
        static_folder='static',
        template_folder='templates'
    )

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/cars')
    def cars():
        return render_template('cars.html')

    @app.route('/booking')
    def booking():
        return render_template('booking.html')

    @app.route('/trips')
    def trips():
        return render_template('trips.html')

    @app.route('/profile')
    def profile():
        return render_template('profile.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return render_template('login.html')

    @app.route('/admin')
    def admin_dashboard():
        return render_template('admin_dashboard.html')

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('500.html'), 500

    # optional: redirect old-style filenames if needed
    @app.route('/index.html')
    def index_html():
        return redirect(url_for('index'))

    @app.route('/cars.html')
    def cars_html():
        return redirect(url_for('cars'))

    @app.route('/booking.html')
    def booking_html():
        return redirect(url_for('booking'))

    @app.route('/trips.html')
    def trips_html():
        return redirect(url_for('trips'))

    @app.route('/profile.html')
    def profile_html():
        return redirect(url_for('profile'))

    @app.route('/login.html')
    def login_html():
        return redirect(url_for('login'))

    @app.route('/admin_dashboard.html')
    def admin_dashboard_html():
        return redirect(url_for('admin_dashboard'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
