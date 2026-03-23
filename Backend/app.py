from flask import Flask, render_template, request, session, redirect, url_for
import os

# We will serve templates from 'templates' and static files from 'static'
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
app.secret_key = 'super_secret_key_for_session_management_here'

# ----------------------------------------------------
# 1. Dummy Login / Role Switcher
# ----------------------------------------------------
@app.route('/dev-login/<role>')
def dev_login(role):
    """
    A temporary developer route to quickly switch roles.
    Go to /dev-login/student or /dev-login/facilitator
    """
    if role in ['student', 'facilitator']:
        session['user_role'] = role
        
        # Redirect based on role
        if role == 'facilitator':
            return redirect(url_for('facilitator'))
        else:
            return redirect(url_for('student'))
            
    return "Invalid role", 400

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ----------------------------------------------------
# 2. Main Pages Rendering
# ----------------------------------------------------
@app.route('/')
def index():
    return render_template('landing.html')

@app.route('/student')
def student():
    # Only allow if logged in and role is 'student'
    role = session.get('user_role')
    if not role:
        # Default to student for testing if no session exists yet
        session['user_role'] = 'student'
        role = 'student'
        
    return render_template('student.html', user_role=role)

@app.route('/facilitator')
def facilitator():
    role = session.get('user_role')
    # If not facilitator, kick them out to student dash
    if role != 'facilitator':
        return redirect(url_for('student'))
        
    return render_template('facilitator.html', user_role=role)

@app.route('/course-modules')
def course_modules():
    role = session.get('user_role', 'student') 
    return render_template('course-modules.html', user_role=role)


# ----------------------------------------------------
# 3. Secure Lesson Rendering (The actual fix)
# ----------------------------------------------------
@app.route('/lesson')
def lesson():
    """ 
    This is what protects the edit toolbar. 
    We pass `is_facilitator` to Jinja based on the secure server session.
    """
    role = session.get('user_role', 'student')
    is_fac = (role == 'facilitator')
    print(f"Viewing lesson. Role: {role}. is_facilitator: {is_fac}")
    
    return render_template('lesson.html', 
                          user_role=role, 
                          is_facilitator=is_fac)

@app.route('/ai-intro')
def ai_intro():
    role = session.get('user_role', 'student')
    is_fac = (role == 'facilitator')
    
    return render_template('ai-intro.html', 
                          user_role=role, 
                          is_facilitator=is_fac)


# Existing API routes
from routes.auth import auth_bp
from routes.user import user_bp
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(user_bp, url_prefix="/api/user")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
