import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import os
from datetime import datetime

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas")
        
        self.tasks = []
        self.load_tasks()
        
        self.task_entry = tk.Entry(root, width=50)
        self.task_entry.pack(pady=10)
        
        self.date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.pack(pady=10)
        
        self.add_task_button = tk.Button(root, text="Adicionar Tarefa", command=self.add_task)
        self.add_task_button.pack(pady=5)
        
        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.pack(pady=10)
        
        self.remove_task_button = tk.Button(root, text="Remover Tarefa", command=self.remove_task)
        self.remove_task_button.pack(pady=5)
        
        self.complete_task_button = tk.Button(root, text="Marcar como Concluída", command=self.complete_task)
        self.complete_task_button.pack(pady=5)
        
        self.edit_task_button = tk.Button(root, text="Editar Tarefa", command=self.edit_task)
        self.edit_task_button.pack(pady=5)
        
        self.filter_var = tk.StringVar(value="Todas")
        
        self.filter_frame = tk.Frame(root)
        self.filter_frame.pack(pady=5)
        
        tk.Radiobutton(self.filter_frame, text="Todas", variable=self.filter_var, value="Todas", command=self.update_task_listbox).pack(side=tk.LEFT)
        tk.Radiobutton(self.filter_frame, text="Pendentes", variable=self.filter_var, value="Pendentes", command=self.update_task_listbox).pack(side=tk.LEFT)
        tk.Radiobutton(self.filter_frame, text="Concluídas", variable=self.filter_var, value="Concluídas", command=self.update_task_listbox).pack(side=tk.LEFT)
        
        self.save_tasks_button = tk.Button(root, text="Salvar Tarefas", command=self.save_tasks)
        self.save_tasks_button.pack(pady=5)

        self.update_task_listbox()
        
    def add_task(self):
        task = self.task_entry.get()
        date = self.date_entry.get_date()
        if task:
            self.tasks.append({"text": task, "completed": False, "date": date.strftime('%Y-%m-%d')})
            self.update_task_listbox()
            self.task_entry.delete(0, tk.END)
            self.date_entry.set_date(datetime.today())
        else:
            messagebox.showwarning("Aviso", "Você deve digitar uma tarefa.")
    
    def remove_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.tasks.pop(selected_task_index)
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Aviso", "Você deve selecionar uma tarefa para remover.")
    
    def complete_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            self.tasks[selected_task_index]["completed"] = True
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Aviso", "Você deve selecionar uma tarefa para marcar como concluída.")
    
    def edit_task(self):
        try:
            selected_task_index = self.task_listbox.curselection()[0]
            task = self.tasks[selected_task_index]
            new_task_text = self.task_entry.get()
            new_task_date = self.date_entry.get_date().strftime('%Y-%m-%d')
            if new_task_text:
                task["text"] = new_task_text
                task["date"] = new_task_date
                self.update_task_listbox()
                self.task_entry.delete(0, tk.END)
                self.date_entry.set_date(datetime.today())
            else:
                messagebox.showwarning("Aviso", "Você deve digitar uma tarefa.")
        except IndexError:
            messagebox.showwarning("Aviso", "Você deve selecionar uma tarefa para editar.")
    
    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        filter_value = self.filter_var.get()
        for task in self.tasks:
            if filter_value == "Todas" or (filter_value == "Pendentes" and not task["completed"]) or (filter_value == "Concluídas" and task["completed"]):
                task_text = f'{task["text"]} - {task["date"]}'
                if task["completed"]:
                    task_text += " (Concluída)"
                self.task_listbox.insert(tk.END, task_text)
    
    def save_tasks(self):
        try:
            with open("tasks.txt", "w") as file:
                for task in self.tasks:
                    file.write(f'{task["text"]}|{task["completed"]}|{task["date"]}\n')
            messagebox.showinfo("Informação", "Tarefas salvas com sucesso.")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar as tarefas: {e}")
    
    def load_tasks(self):
        try:
            if os.path.exists("tasks.txt"):
                with open("tasks.txt", "r") as file:
                    for line in file:
                        parts = line.strip().split("|")
                        if len(parts) == 3:
                            text, completed, date = parts
                            self.tasks.append({"text": text, "completed": completed == "True", "date": date})
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao carregar as tarefas: {e}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = TaskManager(root)
        root.mainloop()
    except Exception as e:
        print(f"Ocorreu um erro ao inicializar a aplicação: {e}")
