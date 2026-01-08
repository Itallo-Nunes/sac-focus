from app import create_app, db
import os

app = create_app()

if __name__ == '__main__':
    # The database needs to be created within the application context
    with app.app_context():
        db.create_all()

    # Get the port number from the environment variable PORT, default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
