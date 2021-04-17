# JetBrains Project - https://hyperskill.org/projects/105?track=2

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')  # create data base
Base = declarative_base()


class Table(Base):  # the class in which we define the columns that will be in the table
    __tablename__ = 'task'  # the name of table
    id = Column(Integer, primary_key=True)  # the id of task
    task = Column(String, default='default_value')  # the task
    deadline = Column(Date, default=datetime.today())  # the deadline tasks

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

run = True
while run:
    print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")
    user_select = input()

    if user_select == '1':  # if you select 1, the program prints the plans for today
        today = datetime.today()
        print(f"\nToday {today.day} {today.strftime('%b')}")
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if len(rows) == 0:  # if there are no plans, we display it
            print("Nothing to do!\n")
            continue
        col = 1
        for row in rows:  # if there is, then we display the tasks
            print(f"{col}. {row}")
            col += 1

    elif user_select == '2':  # with this choice, the program prints tasks scheduled for the week
        date = datetime.today()

        week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        count = 0
        for i in range(7):
            day_after_tomorrow = date + timedelta(days=count)
            rows = session.query(Table).filter(Table.deadline == day_after_tomorrow.date()).all()

            print(f"\n{week_days[day_after_tomorrow.weekday()]} {day_after_tomorrow.day} {day_after_tomorrow.strftime('%b')}:")
            if len(rows) == 0:
                print("Nothing to do!")
            col = 1
            for row in rows:
                print(f"{col}. {row}")
                col += 1

            count += 1
            if count == 7:
                count = 0

    elif user_select == '3':  # all tasks
        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            for i, task in enumerate(rows):
                print('{}. {}. {} {}'.format(i + 1, task, task.deadline.day, task.deadline.strftime('%b')))
        else:
            print('Nothing to do!')

    elif user_select == '4':  # the program prints all expired tasks
        today = datetime.today()
        print('Missed tasks:')
        rows = session.query(Table).filter(Table.deadline < datetime.today().date()).all()
        if rows:
            for i, task in enumerate(rows):
                print('{}. {}. {} {}'.format(i + 1, task, task.deadline.day, task.deadline.strftime('%b')))
        else:
            print('Nothing is missed!')

        session.commit()

    elif user_select == '5':  # here we add tasks
        print('\nEnter task')
        taskes = str(input())
        print('\nEnter deadline')
        deadline = str(input())
        new_row = Table(task=taskes, deadline=datetime.strptime(deadline, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print("The task has been added!")

    elif user_select == '6':  # delete a specific task
        print('Choose the number of the task you want to delete:')

        rows = session.query(Table).order_by(Table.deadline).all()
        if rows:
            for i, task in enumerate(rows):
                print('{}. {}. {} {}'.format(i + 1, task, task.deadline.day, task.deadline.strftime('%b')))
        else:
            print('Nothing to do!')

        number = int(input())

        session.query(Table).filter(Table.id == number).delete()
        print('The task has been deleted!')

        session.commit()

    elif user_select == '0':  # exit the program
        print("\nBye!")
        run = False
        break
        

