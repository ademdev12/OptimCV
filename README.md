# 🚀 OptimCV

OptimCV is a cutting-edge web application meticulously crafted to empower job seekers in their quest for the perfect job. By harnessing the power of advanced Artificial Intelligence (AI) , OptimCV intelligently analyzes your resume (CV) against specific job descriptions, providing a comprehensive compatibility score, generating highly personalized suggestions for improvement, and even delivering an optimized version of your resume tailored to maximize your chances of success. Say goodbye to generic applications and hello to a resume that truly stands out! 
![Home_Page](https://github.com/user-attachments/assets/d312b30e-da11-4eab-a9fb-2e1dd9989a86)



## ✨ Key Features

OptimCV is packed with features designed to give you an edge in the competitive job market:

*   **🎯 Intelligent Resume Optimization**: Upload your CV (in PDF format) and a job offer description. Our AI will analyze both documents to generate a highly optimized version of your resume, ensuring it aligns perfectly with the job requirements.
*   **📊 Dynamic Match Score Calculation**: Instantly receive a compatibility score that quantifies how well your CV matches the job offer. This score helps you understand your strengths and areas for improvement at a glance.
*   **💡 Tailored Improvement Suggestions**: Get actionable, personalized recommendations to enhance your CV's relevance and impact. Our suggestions are designed to help you highlight the most pertinent skills and experiences for each specific role.
*   **🔐 Robust User Authentication**: Enjoy a secure and seamless experience with our comprehensive user authentication system, including easy login, registration, and efficient password management features.
*   **💰 Flexible Subscription Plans**: Choose between our Free and Premium plans, offering varying levels of optimization limits and exclusive features to suit your needs.
*   **📈 Intuitive Dashboard**: Monitor your progress with a personalized dashboard that provides an overview of your optimization history, average match score across all applications, and your current plan's usage progress.
*   **👤 Comprehensive Profile Management**: Easily update your personal information, change your password, and manage your account settings directly from your profile.
*   **💳 Secure Stripe Integration**: Upgrade to our Premium plan effortlessly and securely with our integrated Stripe payment gateway, ensuring a smooth and protected transaction process.




## 🛠️ Technologies Used

OptimCV is built upon a robust and modern technology stack, ensuring high performance, scalability, and a seamless user experience:

*   **🐍 Python**: The core programming language powering the backend logic, data processing, and AI integrations.
*   **🌐 Django**: A powerful, high-level Python web framework that facilitates rapid development of secure and maintainable websites. It handles everything from URL routing to database interactions.
*   **💳 Stripe**: Utilized for secure and efficient payment processing, enabling seamless upgrades to Premium plans.
*   **🧠 Google Generative AI**: The brain behind OptimCV's intelligent analysis and optimization capabilities. This advanced AI model powers the match score calculation, suggestion generation, and resume rewriting.
*   ** Markup & Styling**: The foundation of our user-friendly interface, ensuring a responsive and engaging experience across all devices.
    *   **HTML5**: For structuring the content of the web pages.
    *   **CSS3**: For styling and layout, including responsive design for various screen sizes.
    *   **JavaScript**: For interactive elements and dynamic content on the frontend.
*   **🐘 PostgreSQL**: A powerful, open-source object-relational database system known for its reliability, feature robustness, and performance. It serves as the primary data store for all user and optimization data.




## 🚀 Getting Started

To get OptimCV up and running on your local machine, follow these detailed steps:

### Prerequisites

Before you begin, make sure you have the following software installed on your system:

*   **Python 3.x**: We recommend Python 3.9 or newer for optimal compatibility.
*   **pip**: The Python package installer, usually comes bundled with Python.
*   **PostgreSQL**: A robust relational database system. Ensure it's installed and running, and you have created a database and a user for OptimCV.

### Installation

1.  **Clone the repository**: First, clone the OptimCV repository from GitHub to your local machine using Git:

    ```bash
    git clone https://github.com/ademdev12/OptimCV.git
    cd OptimCV
    ```

2.  **Create a virtual environment**: It's highly recommended to use a virtual environment to manage project dependencies. This isolates your project's dependencies from other Python projects.

    ```bash
    python3 -m venv venv
    ```

3.  **Activate the virtual environment**: Activate the newly created virtual environment:

    *   **On macOS/Linux**:

        ```bash
        source venv/bin/activate
        ```

    *   **On Windows**:

        ```bash
        .\venv\Scripts\activate
        ```

4.  **Install dependencies**: With your virtual environment activated, install all required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up environment variables**: Create a new file named `.env` in the `backend/` directory. This file will store sensitive information and configuration settings. Populate it with the following variables, replacing the placeholder values with your actual keys and settings:

    ```
    SECRET_KEY=your_django_secret_key_here
    DEBUG=True
    STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
    STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key
    GOOGLE_API_KEY=your_google_generative_ai_api_key
    ```

    *   `SECRET_KEY`: A unique, long, and random string used by Django for cryptographic signing. You can generate one using online tools or Python code.
    *   `DEBUG`: Set to `True` for development purposes (enables detailed error pages). **MUST be `False` in production!**
    *   `STRIPE_SECRET_KEY` and `STRIPE_PUBLIC_KEY`: Your secret and public API keys from your Stripe dashboard. These are essential for processing payments.
    *   `GOOGLE_API_KEY`: Your API key for accessing Google Generative AI services. Obtain this from the Google AI Studio or Google Cloud Console.

### Database Setup

1.  **Configure your database**: Open `backend/settings.py` and update the `DATABASES` setting to connect to your PostgreSQL database. Replace the placeholder values with your database credentials:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'OptimCV_db',  # Your database name
            'USER': 'your_db_user',  # Your database username
            'PASSWORD': 'your_db_password',  # Your database password
            'HOST': 'localhost',  # Or your database host
            'PORT': '',  # Leave empty for default, or specify port
        }
    }
    ```

2.  **Apply database migrations**: Run the following commands to create the necessary database tables and apply any pending migrations:

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

3.  **Create a superuser (optional)**: To access the Django administration panel, create a superuser account:

    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set up your username, email, and password.

### Running the Application

1.  **Start the Django development server**: Once all the above steps are completed, you can start the local development server:

    ```bash
    python manage.py runserver
    ```

2.  **Access the application**: Open your web browser and navigate to `http://127.0.0.1:8000/` to access the OptimCV application.




## 💡 Usage Guide

Once you have successfully set up and launched the OptimCV application, here's how you can leverage its powerful features to optimize your job applications:

1.  **🚀 Register or Log In**: Begin by creating a new account if you're a first-time user, or simply log in with your existing credentials to access your personalized dashboard.
2.  **📄 Upload Your CV**: Navigate to the dedicated CV upload section. Here, you will upload your resume (currently, only PDF format is supported) and paste the job offer description for which you want to optimize your CV.
3.  **✨ Optimize Your Resume**: With your CV and job offer uploaded, initiate the optimization process. Our intelligent AI will then analyze both documents in depth:
    *   It will calculate a precise **match score**, indicating the compatibility between your skills and experience and the job requirements.
    *   You will receive a set of **tailored suggestions** designed to help you refine your CV, highlighting keywords and experiences that resonate most with the job description.
    *   For our **Premium users**, OptimCV goes a step further by generating an **optimized version of your CV** in both PDF and DOCX formats, ready for immediate use.
4.  **📊 Monitor Your Progress**: Your personal dashboard provides a comprehensive overview of your optimization activities. Track your past optimizations, view your average match score, and keep an eye on your current subscription plan's usage.
5.  **⚙️ Manage Your Profile**: Access your profile section to update your personal information, change your password, and ensure your account details are always up-to-date.
6.  **💎 Upgrade Your Plan**: If you are on the Free plan and wish to unlock unlimited optimizations and additional premium features (like DOCX output), you can easily upgrade to our Premium plan through a secure and seamless process.




## 🤝 Contributing
Feel free to fork this repository, submit pull requests, or open issues for suggestions, improvements, or bug fixes.


## 📄 License
Distributed under the MIT License.




