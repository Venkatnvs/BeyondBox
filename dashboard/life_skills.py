from django.shortcuts import render

quotes = [
    ("Success is not final, failure is not fatal: It is the courage to continue that counts.", "Winston Churchill"),
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("The future belongs to those who believe in the beauty of their dreams.", "Eleanor Roosevelt"),
    ("Don't watch the clock; do what it does. Keep going.", "Sam Levenson"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("The only limit to our realization of tomorrow will be our doubts of today.", "Franklin D. Roosevelt"),
    ("Success is walking from failure to failure with no loss of enthusiasm.", "Winston Churchill"),
    ("Your time is limited, don't waste it living someone else's life.", "Steve Jobs"),
    ("The biggest risk is not taking any risk.", "Mark Zuckerberg"),
    ("Life is 10% what happens to us and 90% how we react to it.", "Charles R. Swindoll"),
    ("The only person you are destined to become is the person you decide to be.", "Ralph Waldo Emerson"),
    ("You miss 100% of the shots you don't take.", "Wayne Gretzky"),
    ("Strive not to be a success, but rather to be of value.", "Albert Einstein"),
    ("If you want to achieve greatness stop asking for permission.", "Anonymous"),
    ("The journey of a thousand miles begins with one step.", "Lao Tzu"),
    ("Opportunities don't happen, you create them.", "Chris Grosser"),
    ("Success is not the key to happiness. Happiness is the key to success.", "Albert Schweitzer"),
    ("In order to succeed, we must first believe that we can.", "Nikos Kazantzakis"),
    ("Don't be pushed around by the fears in your mind. Be led by the dreams in your heart.", "Roy T. Benne"),
    ("It does not matter how slowly you go as long as you do not stop.", "Confucius"),
    ("The best time to plant a tree was 20 years ago. The second best time is now.", "Chinese Proverb"),
    ("Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.", "Christian D. Larson"),
    ("Success is not in what you have, but who you are.", "Bo Bennett")
]

def LifeSkillsPage(request):
    context = {
        "quotes":quotes
    }
    return render(request,"dashboard/life_skills.html",context)