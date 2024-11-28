function setActionForm(action) {
    const form = document.getElementById("auth-form");
    if (action === "login") {
      form.action = "{{url_for('auth_controller.login')}}";
      form.method = "post";
      form.submit();
    } else if (action === "register") {
      form.action = "{{url_for('auth_controller.register')}}";
      form.method = "post";
      form.submit();
    }
  }