import tkinter as tk
from tkinter import messagebox
import json
import os
import re


class Person:
    def __init__(self, name, surname, age):
        self.name = name
        self.surname = surname
        self.age = age

class Student(Person):
    def __init__(self, name, surname, age):
        super().__init__(name, surname, age)
        self.grades = {}

    def describe(self):
        return f"{self.name} {self.surname} is {self.age} years old"

    def add_grade(self, subject, grade):
        if subject not in self.grades:
            self.grades[subject] = []
        self.grades[subject].append(grade)

    def avg_grade(self):
        grades_total = 0
        count = 0
        for grades in self.grades.values():
            grades_total += sum(grades)
            count += len(grades)
        return grades_total / count if count > 0 else 0

    def subject_average(self, subject):
        if subject in self.grades and self.grades[subject]:
            return sum(self.grades[subject]) / len(self.grades[subject])
        else:
            return 0

    def get_spec(self):
        average = int(self.avg_grade())
        if average >= 9:
            return "Stipresnis studentas"
        elif average >= 7:
            return "Vidutinis studentas"
        else:
            return "Silpnesnis studentas"

    def to_dict(self):
        return {
            "name": self.name,
            "surname": self.surname,
            "age": self.age,
            "grades": self.grades
        }

    @classmethod
    def from_dict(cls, data):
        student = cls(data["name"], data["surname"], data["age"])
        student.grades = data["grades"]
        return student

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Studento Dienynas - Prisijungimas")
        self.geometry("300x250")
        self.students = self.load_data()
        self.current_student = None
        self.login_screen()
        self.subjects = self.load_subjects()


    def save_data(self):
        
        data = {name: student.to_dict() for name, student in self.students.items()}
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

    def load_data(self):
        
        if os.path.exists("data.json"):
            with open("data.json", "r") as file:
                data = json.load(file)
                return {name: Student.from_dict(info) for name, info in data.items()}
        else:
            
            return {}

    def login_screen(self):
        
        for widget in self.winfo_children():
            widget.destroy()
        
        tk.Label(self, text="Pasirinkite vartotojo tipą").pack(pady=5)
        
        
        self.user_type = tk.StringVar()
        tk.Radiobutton(self, text="Studentas", variable=self.user_type, value="studentas").pack()
        tk.Radiobutton(self, text="Dėstytojas", variable=self.user_type, value="dėstytojas").pack()

        
        tk.Label(self, text="Vartotojo vardas").pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        tk.Label(self, text="Slaptažodis").pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self, text="Prisijungti", command=self.check_login)
        login_button.pack(pady=10)

    def check_login(self):
        user_type = self.user_type.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        
        if user_type == "studentas" and username in self.students and password == "dienynas123":
            self.current_student = self.students[username]
            self.main_screen_student()
        elif user_type == "dėstytojas" and username == "destytojas" and password == "slaptazodis456":
            self.main_screen_teacher()
        else:
            messagebox.showerror("Klaida", "Neteisingas vartotojo vardas arba slaptažodis!")

    def main_screen_student(self):
        
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Sveiki prisijungę į studento dienyną!", font=("Arial", 14)).pack(pady=10)
        
        view_grades_button = tk.Button(self, text="Pažymių peržiūra", command=self.view_grades)
        view_grades_button.pack(pady=5)

        view_averages_button = tk.Button(self, text="Vidurkių peržiūra", command=self.view_averages)
        view_averages_button.pack(pady=5)

        view_subjects_button = tk.Button(self, text="Dalykų peržiūra", command=self.view_subjects)
        view_subjects_button.pack(pady=5)

        logout_button = tk.Button(self, text="Atsijungti", command=self.login_screen)
        logout_button.pack(pady=10)

    def main_screen_teacher(self):
        
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Sveiki, dėstytojau!", font=("Arial", 14)).pack(pady=10)
        
        tk.Button(self, text="Visų studentų peržiūra", command=self.view_all_students).pack(pady=5)
        tk.Button(self, text="Pridėti studentą", command=self.add_student).pack(pady=5)
        tk.Button(self, text="Pašalinti studentą", command=self.remove_student).pack(pady=5)
        tk.Button(self, text="Rasti studentą", command=self.find_student).pack(pady=5)
        tk.Button(self, text="Įrašyti pažymį studentui", command=self.add_grade).pack(pady=5)
        tk.Button(self, text="Pridėti dalyką", command=self.add_subject).pack(pady=5)
        tk.Button(self, text="Pašalinti dalyką", command=self.delete_subject).pack(pady=5)
        tk.Button(self, text="Priskirti dalyką studentui", command=self.assign_subject).pack(pady=5)
        tk.Button(self, text="Peržiūrėti dalykus", command=self.view_subjects_teacher).pack(pady=5)
        tk.Button(self, text="Pašalinti dalyką iš studento", command=self.remove_subject_from_student).pack(pady=5)
        tk.Button(self, text="Atsijungti", command=self.login_screen).pack(pady=10)

    def add_student(self):
        
        self.clear_window()
        tk.Label(self, text="Pridėti naują studentą", font=("Arial", 12)).pack(pady=10)
        
        tk.Label(self, text="Vardas:").pack()
        self.new_student_name_entry = tk.Entry(self)
        self.new_student_name_entry.pack(pady=5)

        tk.Label(self, text="Pavardė:").pack()
        self.new_student_surname_entry = tk.Entry(self)
        self.new_student_surname_entry.pack(pady=5)

        tk.Label(self, text="Amžius:").pack()
        self.new_student_age_entry = tk.Entry(self)
        self.new_student_age_entry.pack(pady=5)

        save_button = tk.Button(self, text="Išsaugoti studentą", command=self.save_student)
        save_button.pack(pady=5)

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_teacher)
        back_button.pack(pady=10)

    def save_student(self):
        
        name = self.new_student_name_entry.get()
        surname = self.new_student_surname_entry.get()
        age = self.new_student_age_entry.get()

        if not name or not surname or not age.isdigit():
            messagebox.showerror("Klaida", "Užpildykite visus laukus teisingai.")
            return

        if name in self.students:
            messagebox.showerror("Klaida", "Studentas su tokiu vardu jau egzistuoja.")
            return

        age = int(age)
        self.students[name] = Student(name, surname, age)
        self.save_data()
        messagebox.showinfo("Sėkmė", f"Studentas {name} {surname} pridėtas sėkmingai!")

    def remove_student(self):
        
        self.clear_window()
        tk.Label(self, text="Pašalinti studentą", font=("Arial", 12)).pack(pady=10)
        
        tk.Label(self, text="Studento vardas:").pack()
        self.remove_student_name_entry = tk.Entry(self)
        self.remove_student_name_entry.pack(pady=5)

        remove_button = tk.Button(self, text="Pašalinti studentą", command=self.delete_student)
        remove_button.pack(pady=5)

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_teacher)
        back_button.pack(pady=10)

    def delete_student(self):
        
        name = self.remove_student_name_entry.get()

        if name in self.students:
            del self.students[name]
            self.save_data()
            messagebox.showinfo("Sėkmė", f"Studentas {name} pašalintas sėkmingai!")
        else:
            messagebox.showerror("Klaida", "Studentas nerastas.")

    def find_student(self):
        self.clear_window()
        tk.Label(self, text="Įveskite studento vardą:", font=("Arial", 12)).pack(pady=5)
    
        self.student_name_entry = tk.Entry(self)
        self.student_name_entry.pack(pady=5)

        search_button = tk.Button(self, text="Ieškoti", command=self.display_student_grades)
        search_button.pack(pady=5)

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_teacher)
        back_button.pack(pady=10)

    def display_student_grades(self):
        
        student_name = self.student_name_entry.get()

        
        name_pattern = re.compile(r"^[A-Za-z]+$")
        if not name_pattern.match(student_name):
            messagebox.showerror("Klaida", "Neteisingas studento vardas! Įveskite tik raides.")
            return

        self.clear_window()
    
        tk.Label(self, text=f"Pažymiai studentui: {student_name}", font=("Arial", 12)).pack(pady=10)
    
        if student_name in self.students:
            student = self.students[student_name]
        
            
            specialization = student.get_spec()
            tk.Label(self, text=f"Specializacija: {specialization}").pack(pady=5)
        
           
            grades = student.grades
            for subject, grade in grades.items():
                tk.Label(self, text=f"{subject}: {grade}").pack()
        else:
            tk.Label(self, text="Studentas nerastas").pack()

        back_button = tk.Button(self, text="Atgal", command=self.find_student)
        back_button.pack(pady=10)


    def view_grades(self):
        
        self.clear_window()
        tk.Label(self, text="Pažymių peržiūra", font=("Arial", 12)).pack(pady=10)
        for subject, grades in self.current_student.grades.items():
            tk.Label(self, text=f"{subject}: {grades}").pack()

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_student)
        back_button.pack(pady=10)

    def view_averages(self):
        
        self.clear_window()
        tk.Label(self, text="Vidurkių peržiūra", font=("Arial", 12)).pack(pady=10)
        for subject in self.current_student.grades:
            avg = self.current_student.subject_average(subject)
            tk.Label(self, text=f"{subject} vidurkis: {avg:.2f}").pack()

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_student)
        back_button.pack(pady=10)

    def view_subjects(self):
        
        self.clear_window()
        tk.Label(self, text="Dalykų peržiūra", font=("Arial", 12)).pack(pady=10)
        for subject in self.current_student.grades:
            tk.Label(self, text=subject).pack()

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_student)
        back_button.pack(pady=10)
        
    def remove_subject_from_student(self):
        
        self.clear_window()
        tk.Label(self, text="Ištrinti dalyką iš studento", font=("Arial", 12)).pack(pady=10)

        tk.Label(self, text="Studento vardas:").pack()
        self.student_name_entry = tk.Entry(self)
        self.student_name_entry.pack(pady=5)

        tk.Label(self, text="Dalyko pavadinimas:").pack()
        self.subject_name_entry = tk.Entry(self)
        self.subject_name_entry.pack(pady=5)

        remove_button = tk.Button(self, text="Pašalinti dalyką", command=self.delete_subject_from_student)
        remove_button.pack(pady=5)

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_teacher)
        back_button.pack(pady=10)

    def delete_subject_from_student(self):
        
        student_name = self.student_name_entry.get()
        subject_name = self.subject_name_entry.get()

        
        if student_name not in self.students:
            messagebox.showerror("Klaida", f"Studentas '{student_name}' nerastas.")
            return

        
        student = self.students[student_name]
        if subject_name not in student.grades:
            messagebox.showerror("Klaida", f"Dalykas '{subject_name}' nerastas studento '{student_name}' sąraše.")
            return

        
        del student.grades[subject_name]
        self.save_data()
        messagebox.showinfo("Sėkmė", f"Dalykas '{subject_name}' pašalintas iš studento '{student_name}' įrašų.")
 

    def view_all_students(self):
        
        self.clear_window()
        tk.Label(self, text="Visi studentai", font=("Arial", 12)).pack(pady=10)
        for student in self.students.values():
            tk.Label(self, text=student.describe()).pack()

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_teacher)
        back_button.pack(pady=10)

    def find_student(self):
        
        self.clear_window()
        tk.Label(self, text="Įveskite studento vardą:", font=("Arial", 12)).pack(pady=5)
        
        self.student_name_entry = tk.Entry(self)
        self.student_name_entry.pack(pady=5)

        search_button = tk.Button(self, text="Ieškoti", command=self.display_student_grades)
        search_button.pack(pady=5)

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_teacher)
        back_button.pack(pady=10)

    def display_student_grades(self):
        
        student_name = self.student_name_entry.get()

        
        name_pattern = re.compile(r"^[A-Za-z]+$")
        if not name_pattern.match(student_name):
            messagebox.showerror("Klaida", "Neteisingas studento vardas! Įveskite tik raides.")
            return

        self.clear_window()
        
        tk.Label(self, text=f"Pažymiai studentui: {student_name}", font=("Arial", 12)).pack(pady=10)
        
        if student_name in self.students:
            student = self.students[student_name]
            
            
            specialization = student.get_spec()
            tk.Label(self, text=f"Specializacija: {specialization}").pack(pady=5)
            
            
            grades = student.grades
            for subject, grade in grades.items():
                tk.Label(self, text=f"{subject}: {grade}").pack()
        else:
            tk.Label(self, text="Studentas nerastas").pack()

        back_button = tk.Button(self, text="Atgal", command=self.find_student)
        back_button.pack(pady=10)

    def add_grade(self):
        
        self.clear_window()
        tk.Label(self, text="Pasirinkite studentą ir įveskite pažymį:", font=("Arial", 12)).pack(pady=10)
        
        tk.Label(self, text="Studento vardas:").pack()
        self.grade_student_name_entry = tk.Entry(self)
        self.grade_student_name_entry.pack(pady=5)

        tk.Label(self, text="Dalykas:").pack()
        self.subject_entry = tk.Entry(self)
        self.subject_entry.pack(pady=5)

        tk.Label(self, text="Pažymys:").pack()
        self.grade_entry = tk.Entry(self)
        self.grade_entry.pack(pady=5)

        save_button = tk.Button(self, text="Išsaugoti pažymį", command=self.save_grade)
        save_button.pack(pady=5)

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_teacher)
        back_button.pack(pady=10)

    def save_grade(self):
        
        student_name = self.grade_student_name_entry.get()
        subject = self.subject_entry.get()
        grade = self.grade_entry.get()

        
        grade_pattern = re.compile(r"^\d+$")
        
        if student_name in self.students:
            if grade_pattern.match(grade):  
                grade = int(grade)  
                self.students[student_name].add_grade(subject, grade)
                self.save_data()  
                messagebox.showinfo("Išsaugota", f"Pažymys {grade} pridėtas dalykui {subject} studentui {student_name}")
            else:
                messagebox.showerror("Klaida", "Įveskite galiojantį pažymį (skaičius).")
        else:
            messagebox.showerror("Klaida", "Studentas nerastas")

    def clear_window(self):
        
        for widget in self.winfo_children():
            widget.destroy()
            
    def add_subject(self):
       
        self.clear_window()
        tk.Label(self, text="Pridėti naują dalyką", font=("Arial", 12)).pack(pady=10)

        tk.Label(self, text="Dalyko pavadinimas:").pack()
        self.new_subject_entry = tk.Entry(self)
        self.new_subject_entry.pack(pady=5)

        save_button = tk.Button(self, text="Išsaugoti dalyką", command=self.save_new_subject)
        save_button.pack(pady=5)

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_teacher)
        back_button.pack(pady=10)

    def save_new_subject(self):
        
        subject = self.new_subject_entry.get()
        if not subject or subject in self.subjects:
            messagebox.showerror("Klaida", "Dalykas jau egzistuoja arba laukas tuščias.")
            return
        self.subjects.append(subject)
        self.save_subjects()
        messagebox.showinfo("Sėkmė", f"Dalykas '{subject}' pridėtas sėkmingai!")
        
            
    def save_subjects(self):
    
     with open("subjects.json", "w") as file:
            json.dump(self.subjects, file, indent=4)

    def load_subjects(self):
    
        if os.path.exists("subjects.json"):
            with open("subjects.json", "r") as file:
             return json.load(file)
        else:
            return []

    def delete_subject(self):
        
        self.clear_window()
        tk.Label(self, text="Pašalinti dalyką", font=("Arial", 12)).pack(pady=10)

        tk.Label(self, text="Dalyko pavadinimas:").pack()
        self.delete_subject_entry = tk.Entry(self)
        self.delete_subject_entry.pack(pady=5)

        delete_button = tk.Button(self, text="Pašalinti dalyką", command=self.remove_subject)
        delete_button.pack(pady=5)

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_teacher)
        back_button.pack(pady=10)

    def remove_subject(self):
        
        subject = self.delete_subject_entry.get()
        if subject in self.subjects:
            
            self.subjects.remove(subject)
            self.save_subjects()

           
            for student in self.students.values():
                if subject in student.grades:
                    del student.grades[subject]

            
            self.save_data()

            messagebox.showinfo("Sėkmė", f"Dalykas '{subject}' pašalintas sėkmingai ir pašalintas iš visų studentų įrašų!")
        else:
            messagebox.showerror("Klaida", "Toks dalykas nerastas.")

            
    def assign_subject(self):
        
        self.clear_window()
        tk.Label(self, text="Priskirti dalyką studentui", font=("Arial", 12)).pack(pady=10)

        tk.Label(self, text="Studento vardas:").pack()
        self.assign_student_name_entry = tk.Entry(self)
        self.assign_student_name_entry.pack(pady=5)

        tk.Label(self, text="Dalyko pavadinimas:").pack()
        self.assign_subject_name_entry = tk.Entry(self)
        self.assign_subject_name_entry.pack(pady=5)

        assign_button = tk.Button(self, text="Priskirti dalyką", command=self.add_subject_to_student)
        assign_button.pack(pady=5)

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_teacher)
        back_button.pack(pady=10)

    def add_subject_to_student(self):
        
        student_name = self.assign_student_name_entry.get()
        subject = self.assign_subject_name_entry.get()

        if student_name not in self.students:
            messagebox.showerror("Klaida", "Studentas nerastas.")
            return

        if subject not in self.subjects:
            messagebox.showerror("Klaida", "Dalykas nerastas. Pridėkite dalyką pirmiausia.")
            return

        student = self.students[student_name]

        if subject not in student.grades:
            student.grades[subject] = []
            self.save_data()
            messagebox.showinfo("Sėkmė", f"Dalykas '{subject}' priskirtas studentui {student_name}.")
        else:
            messagebox.showerror("Klaida", f"Studentas jau turi dalyką '{subject}'.")
    
    def view_subjects_teacher(self):
        self.clear_window()
        tk.Label(self, text="Visi dalykai", font=("Arial", 12)).pack(pady=10)

        if self.subjects:
            for subject in self.subjects:
                tk.Label(self, text=subject).pack(pady=5)
        else:
            tk.Label(self, text="Dalykų sąrašas tuščias.").pack(pady=5)

        back_button = tk.Button(self, text="Atgal", command=self.main_screen_teacher)
        back_button.pack(pady=10)



app = LoginApp()
app.mainloop()
