from fasthtml.common import *

def render(todo):
    tid = f'todo-{todo.id}'
    toggle = A('Toggle', hx_get=f'/database/{todo.id}', target_id=tid)
    delete = A('Delete', hx_delete=f'/database/{todo.id}', hx_swap='outerHTML', target_id=tid)
    return Li(toggle, delete, todo.title + (' ✨' if todo.done else ''), id=tid)


app, rt, todos, Todo = fast_app('todos.db',
                                live=True,
                                id=int,        #db type of primary key
                                pk='id',       #db primary key
                                title=str,     #db inserting
                                done=bool,     #db
                                render=render) #db
@rt("/database")
def get():
    #todos.insert(Todo(title='Fist todo', done=False))
    frm = Form(Group(Input(placeholder='Add a new todo', name='title'), Button("Add")),
                      hx_post='/database', target_id='todo-list', hx_swap='beforeend')
    return Titled('Todos', Card(Ul(*todos(), id='todo-list'),  header=frm)
                  )
@rt("/database")
def post(todo:Todo):
    return todos.insert(todo)

@rt("/database/{tid}")
def delete(tid:int):
    return todos.delete(tid)


@rt("/database/{tid}")
def get(tid:int):
    todo = todos[tid]
    #todos.insert(Todo(title='Fist todo', done=False))
    todo.done = not todo.done
    todos.update(todo)
    return todo

@rt("/")
def get():
    desc = 100
    return Titled(Div('FAST',
                      H1("Hello fastHTML"),
                      Div("Like it for", id='stuff', hx_get='/change'),
                      P(f"-->{desc}%"),
                      P(A('Link', href='/change')),
                      P(A('Database', href='/database')),
                      )
                  )
@rt("/change")
def get():
    return Titled('Change',
                  P('Change is super'),
                  P(A('Home', href='/'))
                  )

serve()