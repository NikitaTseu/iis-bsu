#!/usr/bin/env python
# coding: utf-8

# In[69]:


textures = ["жидкое", "твердое"]
tastes = ["сладкое", "острое"]
temperatures = ["холодное", "горячее"]
types = ["напиток", "суп", "десерт"]
maincourse = ["основное блюдо", "не основное блюдо"]

countries = ["Россия", "Франция", "Турция", "Таиланд", 
             "Венгрия", "Япония", "Германия"]

names = ["эклер", "мороженое", "рахат-лукум", "окрошка", "том-ям", "гуляш",
         "рамен", "сбитень", "квас", "пиво", "суши", "чай"]

attrs = {'taste': tastes, 'texture': textures, 'temperature': temperatures, 
         'type': types, 'country': countries, 
         'name': names, 'maincourse': maincourse}

questions = {'taste': 'Какое это блюдо на вкус?', 
             'texture': 'Какое это блюдо по текстуре?', 
             'temperature': 'Как подается это блюдо?', 
             'type': 'Как бы вы охаректиризовали тип этого блюда?', 
             'country': 'В какой стране это блюдо считается традиционным?', 
             'maincourse': 'Это основное блюдо?'}


# In[70]:


class Rule:
    def __init__(self, facts, info):
        self.facts = facts
        self.info = info
    
    def __str__(self):
        s = 'IF \'' + self.facts[0][0] + ' = ' + self.facts[0][1] + '\''
        for fact in self.facts[1:]:
            s = s + ' AND \'' + fact[0] + ' = ' + fact[1] + '\''
        s = s + ' THEN \'' + self.info[0] + ' = ' + self.info[1] + '\''
        return s


# In[71]:


rules = []

rules.append(Rule([('texture', 'жидкое'), ('maincourse', 'основное блюдо')], 
                  ('type', 'суп')))

rules.append(Rule([('texture', 'жидкое'), ('maincourse', 'не основное блюдо')], 
                  ('type', 'напиток')))

rules.append(Rule([('texture', 'твердое'), ('maincourse', 'не основное блюдо')], 
                  ('type', 'десерт')))

rules.append(Rule([('type', 'десерт'), ('country', 'Франция')], 
                  ('name', 'эклер')))

rules.append(Rule([('type', 'десерт'), ('country', 'Турция')], 
                  ('name', 'рахат-лукум')))

rules.append(Rule([('type', 'десерт'), ('temperature', 'холодное')], 
                  ('name', 'эклер')))

rules.append(Rule([('type', 'суп'), ('temperature', 'холодное')], 
                  ('name', 'окрошка')))

rules.append(Rule([('type', 'суп'), ('country', 'Япония')], 
                  ('name', 'рамен')))

rules.append(Rule([('type', 'суп'), ('country', 'Таиланд'), ('taste', 'острое')], 
                  ('name', 'том-ям')))

rules.append(Rule([('type', 'суп'), ('country', 'Венгрия'), ('taste', 'острое')], 
                  ('name', 'гуляш')))

rules.append(Rule([('type', 'напиток'), ('country', 'Россия'), ('temperature', 'горячее')], 
                  ('name', 'сбитень')))

rules.append(Rule([('type', 'напиток'), ('country', 'Россия'), ('temperature', 'холодное')], 
                  ('name', 'квас')))

rules.append(Rule([('type', 'напиток'), ('country', 'Германия'), ('temperature', 'холодное')], 
                  ('name', 'пиво')))

rules.append(Rule([('type', 'напиток'), ('country', 'Турция'), ('temperature', 'горячее')], 
                  ('name', 'чай')))

rules.append(Rule([('texture', 'твердое'), ('country', 'Япония')], 
                  ('name', 'суши')))


# In[72]:


from tkinter import *
import random


# In[73]:


def think():
    messages = ["Хммм... \n", 
                "Давай-ка подумаем... \n", 
                "Что бы еще спросить... \n", 
                "Даже не знаю... \n", 
                "Ну и задачку ты мне подкинул... \n"]
    
    index = random.randint(0, len(messages) - 1)
    return messages[index]


# In[74]:


target = 'name'
target_stack = []
ruleset_all = []
context_stack = []


# In[75]:


def init():
    global target
    global target_stack
    global ruleset_all
    global rules
    global context_stack
    
    fl = names[0]
    for food in names[1:]:
        fl = fl + ', ' + food
    
    food_list.configure(text = fl)
    
    ruleset_all = []
    for rule in rules:
        # логический флаг определяет, использовалось ли уже это правило для анализа
        ruleset_all.append([rule, False])
    
    target = 'name'

    target_stack = []
    context_stack = []
    target_stack.append([target, -1])
    
def reload():
    global widgets
    
    for w in widgets:
        w.place_forget()

def start_game():
    init()
    reload()
    text.configure(text = "Готовы начать игру?")
    
    text.place(x=60, y=50)
    start_btn.place(x=120, y=100)
    
def choose_food():
    reload()
    text.configure(text = "Загадайте какое-нибудь блюдо. \n На данный момент я владею информацией о следующих блюдах: \n ")
    text.place(x=60, y=50)
    food_list.place(x=80, y=145)
    start_btn_2.place(x=80, y=220)
    
    
def start_algo():
    reload()
    game_step()
    
def lose_game():
    reload()
    text.configure(text = "Сдаюсь, не могу отгадать твоё блюдо")
    text.place(x=60, y=50)
    new_game_btn.place(x=120, y=100)


def win_game(ans):
    reload()
    text.configure(text="Я думаю, что ты загадал " + ans)
    text.place(x=60, y=50)
    new_game_btn.place(x=120, y=100)


def game_step():
    global target
    global target_stack
    global ruleset_all
    global rules
    global context_stack
    
    while(find_rule(target_stack[-1][0]) != -1000):
        current_rule_index = find_rule(target_stack[-1][0])
        current_rule = ruleset_all[current_rule_index][0]
        
        rule_status = check_rule(current_rule_index)
        if(rule_status == 1):
            context_stack.append(current_rule.info)
            if(len(target_stack) > 1):
                del target_stack[-1]
            else:
                win_game(context_stack[-1][1])
                return 0
            
    if(target_stack[-1][0] == target):
        lose_game()
        return 0
    else:
        ask_for_help(target_stack[-1][0])

def help_received():
    global target
    global target_stack
    global ruleset_all
    global rules
    global context_stack
    
    ans = combo.get()
    current_target = target_stack[-1][0]
    current_rule_index = target_stack[-1][1]
    del target_stack[-1]
    context_stack.append((current_target, ans))
    if(len(target_stack) > 1):

        current_rule = ruleset_all[current_rule_index][0]
        
        rule_status = check_rule(current_rule_index)
        if(rule_status == 1):
            context_stack.append(current_rule.info)
            if(len(target_stack) > 1):
                del target_stack[-1]
            else:
                win_game(context_stack[-1][1])
        
    game_step()

def ask_for_help(target_type):
    global target
    global target_stack
    global ruleset_all
    global rules
    global context_stack
    
    reload()
    
    text.configure(text = think() + questions[target_type])
    combo['values'] = attrs[target_type]
    combo.current(1)

    text.place(x=60, y=50)
    combo.place(x=90, y=150)
    help_received_btn.place(x=120, y=180)


# In[78]:


def find_rule(target_type):
    global target
    global target_stack
    global ruleset_all
    global rules
    global context_stack
    
    for i in range(len(ruleset_all)):
        rule_pair = ruleset_all[i]
        if(rule_pair[1] == False and rule_pair[0].info[0] == target_type):
            return i
    return -1000;


# In[79]:


# 0 - правило ложно
# 1 - правило истинно
# 2 - значение правила неизвестно

def check_rule(i):
    global target
    global target_stack
    global ruleset_all
    global rules
    global context_stack
    
    #ruleset_all[i][1] = True
    rule = ruleset_all[i][0]
    for fact in rule.facts:
        fact_approved = False
        for known_fact in context_stack:
            if (known_fact[0] == fact[0] and known_fact[1] != fact[1]):
                ruleset_all[i][1] = True
                return 0
            if (known_fact[0] == fact[0] and known_fact[1] == fact[1]):
                fact_approved = True
        if(not fact_approved):
            target_stack.append([fact[0], i])
            #debug_target_stack()
            return 2
    ruleset_all[i][1] = True
    return 1


# In[80]:


def debug_target_stack():
    print("==================")
    print("TARGET STACK")
    for x in target_stack:
        print(x)
    print("==================")


# In[ ]:


from tkinter import ttk

window = Tk()
window.title("Угадай блюдо")
window.geometry("600x400")

text = Message(window, width = 450, fg='black', font=("Helvetica", 18))
food_list = Message(window, width = 450, fg='black', font=("Helvetica", 12))
start_btn = Button(window, text="Поехали!", bg = 'white', fg='blue', command = choose_food, font=("Helvetica", 12))
start_btn_2 = Button(window, text="Загадал, давай начинать", bg = 'white', fg='blue', command = start_algo, font=("Helvetica", 12))
help_received_btn = Button(window, text="Готово", bg = 'white', fg='blue', command = help_received, font=("Helvetica", 12))
new_game_btn = Button(window, text="Сыграть еще раз", bg = 'white', fg='blue', command = start_game, font=("Helvetica", 12))
combo = ttk.Combobox(window)

widgets = [text, food_list, start_btn, start_btn_2, help_received_btn, new_game_btn, combo]

start_game()

window.mainloop()


# In[ ]:




