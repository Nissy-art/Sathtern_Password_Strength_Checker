import tkinter as tk
from tkinter import ttk
import string
import secrets
import re


# -----------------------------
# Password Analysis
# -----------------------------
def analyze_password(password):
    checks = {
        "Minimum 8 characters": len(password) >= 8,
        "Uppercase letter": bool(re.search(r"[A-Z]", password)),
        "Lowercase letter": bool(re.search(r"[a-z]", password)),
        "Number": bool(re.search(r"\d", password)),
        "Special character": bool(re.search(r"[^A-Za-z0-9]", password)),
    }

    score = sum(checks.values())

    common_passwords = {
        "password",
        "password123",
        "123456",
        "12345678",
        "qwerty",
        "qwerty123",
        "admin",
        "admin123",
        "welcome",
        "letmein",
    }

    if not password:
        strength = "No Password"
    elif password.lower() in common_passwords:
        strength = "Very Weak"
    elif score <= 2:
        strength = "Weak"
    elif score == 3:
        strength = "Moderate"
    elif score == 4:
        strength = "Strong"
    else:
        strength = "Very Strong"

    return checks, strength


# -----------------------------
# Check Password Button
# -----------------------------
def check_password():
    password = password_entry.get()

    checks, strength = analyze_password(password)

    strength_label.config(text=f"Strength: {strength}")

    # Update checklist
    for requirement, passed in checks.items():
        symbol = "✓" if passed else "✗"
        status = "PASS" if passed else "FAIL"
        requirement_labels[requirement].config(
            text=f"{symbol} {requirement} - {status}"
        )

    # Security message
    if not password:
        message_label.config(
            text="Please enter a password.",
        )
    elif strength in ("Very Weak", "Weak"):
        message_label.config(
            text="⚠ This password is weak. Consider using a stronger password."
        )
    elif strength == "Moderate":
        message_label.config(
            text="Your password is acceptable, but it can be stronger."
        )
    else:
        message_label.config(
            text="✓ Good password! It satisfies the security requirements."
        )


# -----------------------------
# Generate Strong Password
# -----------------------------
def generate_password():
    length = 16

    # Guarantee all required character types
    required_characters = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]

    all_characters = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    remaining_characters = [
        secrets.choice(all_characters)
        for _ in range(length - len(required_characters))
    ]

    password_characters = required_characters + remaining_characters

    # Securely shuffle the password characters
    secrets.SystemRandom().shuffle(password_characters)

    generated = "".join(password_characters)

    password_entry.delete(0, tk.END)
    password_entry.insert(0, generated)

    check_password()


# -----------------------------
# Show / Hide Password
# -----------------------------
def toggle_password():
    if password_entry.cget("show") == "":
        password_entry.config(show="*")
        show_button.config(text="Show")
    else:
        password_entry.config(show="")
        show_button.config(text="Hide")


# -----------------------------
# Clear
# -----------------------------
def clear_password():
    password_entry.delete(0, tk.END)

    strength_label.config(text="Strength: —")

    for requirement in requirement_labels:
        requirement_labels[requirement].config(
            text=f"○ {requirement}"
        )

    message_label.config(text="Enter a password to begin.")


# -----------------------------
# Copy Generated Password
# -----------------------------
def copy_password():
    password = password_entry.get()

    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()

        message_label.config(
            text="✓ Password copied to clipboard."
        )


# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()

root.title("Password Security Checker")
root.geometry("620x650")
root.resizable(False, False)

# -----------------------------
# Header
# -----------------------------
header = tk.Label(
    root,
    text="🔐 PASSWORD SECURITY CHECKER",
    font=("Arial", 22, "bold"),
)

header.pack(pady=(25, 5))

subtitle = tk.Label(
    root,
    text="Check password strength and generate secure passwords",
    font=("Arial", 11),
)

subtitle.pack(pady=(0, 20))


# -----------------------------
# Password Section
# -----------------------------
password_frame = tk.Frame(root)
password_frame.pack(pady=10)

password_label = tk.Label(
    password_frame,
    text="Enter Password:",
    font=("Arial", 12, "bold"),
)

password_label.grid(row=0, column=0, padx=5)


password_entry = tk.Entry(
    password_frame,
    width=32,
    font=("Arial", 12),
    show="*",
)

password_entry.grid(row=0, column=1, padx=5)


show_button = tk.Button(
    password_frame,
    text="Show",
    width=7,
    command=toggle_password,
)

show_button.grid(row=0, column=2, padx=5)


# -----------------------------
# Buttons
# -----------------------------
button_frame = tk.Frame(root)
button_frame.pack(pady=15)

check_button = tk.Button(
    button_frame,
    text="Check Password",
    width=16,
    command=check_password,
)

check_button.grid(row=0, column=0, padx=5)

generate_button = tk.Button(
    button_frame,
    text="Generate Strong Password",
    width=22,
    command=generate_password,
)

generate_button.grid(row=0, column=1, padx=5)


# -----------------------------
# Strength
# -----------------------------
strength_label = tk.Label(
    root,
    text="Strength: —",
    font=("Arial", 16, "bold"),
)

strength_label.pack(pady=10)


# -----------------------------
# Requirements
# -----------------------------
requirements_title = tk.Label(
    root,
    text="Password Requirements",
    font=("Arial", 14, "bold"),
)

requirements_title.pack(pady=(15, 5))


requirements_frame = tk.Frame(root)
requirements_frame.pack()

requirements = [
    "Minimum 8 characters",
    "Uppercase letter",
    "Lowercase letter",
    "Number",
    "Special character",
]

requirement_labels = {}

for requirement in requirements:
    label = tk.Label(
        requirements_frame,
        text=f"○ {requirement}",
        font=("Arial", 11),
        anchor="w",
        width=35,
    )

    label.pack(anchor="w")

    requirement_labels[requirement] = label


# -----------------------------
# Message
# -----------------------------
message_label = tk.Label(
    root,
    text="Enter a password to begin.",
    font=("Arial", 11),
    wraplength=520,
)

message_label.pack(pady=20)


# -----------------------------
# Bottom Buttons
# -----------------------------
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

copy_button = tk.Button(
    bottom_frame,
    text="Copy Password",
    width=15,
    command=copy_password,
)

copy_button.grid(row=0, column=0, padx=5)


clear_button = tk.Button(
    bottom_frame,
    text="Clear",
    width=15,
    command=clear_password,
)

clear_button.grid(row=0, column=1, padx=5)


# -----------------------------
# Footer
# -----------------------------
footer = tk.Label(
    root,
    text="Sathern Cybersecurity Internship • Password Security Tool",
    font=("Arial", 9),
)

footer.pack(side="bottom", pady=15)


# -----------------------------
# Run Application
# -----------------------------
root.mainloop()