    app.config.from_object(Config)

    init_scheduler(app)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    @app.teardown_appcontext
    def shutdown_session(exception=None):