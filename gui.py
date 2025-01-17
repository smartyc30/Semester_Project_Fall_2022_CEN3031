import PySimpleGUI as sg
import auth

auth.data.get_users_from_file()
def login_window(window):
    while True:
        window['-LOGIN-'].update(visible=True)
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event in 'Login':
            if auth.login(values['-USER-'], values['-PASS-']):
                window['-LOGIN-'].update(visible=False)
                home_window(window)
            else:
                sg.popup_ok('Incorrect username or password.', 'Please try again.',
                            background_color='#B7CECE', title='Error')
                continue
        elif event in 'Create New User':
            window['-LOGIN-'].update(visible=False)
            new_user_window(window)
    window.close()
    exit(0)


def new_user_window(window):
    while True:
        window['-CREATE-'].update(visible=True)
        event, values = window.read()
        if event == '__TITLEBAR CLOSE__3':
            break
        elif event in 'Create':
            user_created = auth.new_user(values['-NEW USER-'], values['-NEW PASS-'], values['-PASS_CONF-'])
            if user_created == auth.NewUserOptions.USER_EXISTS:
                sg.popup_ok('This username is already in use.', 'Please try again.',
                            background_color='#B7CECE', title='Error')
                continue
            elif user_created == auth.NewUserOptions.PAS_MISMATCH:
                sg.popup_ok('The passwords you entered do not match.', 'Please try again.',
                            background_color='#B7CECE', title='Error')
                continue
            elif user_created == auth.NewUserOptions.USER_CREATED:
                sg.popup('New user created successfully', background_color='#B7CECE', title='Success')
                window['-CREATE-'].update(visible=False)
                login_window(window)
        elif event in 'Cancel':
            window['-CREATE-'].update(visible=False)
            login_window(window)
    window.close()
    exit(0)


def home_window(window):
    while True:
        window['-HOME-'].update(visible=True)
        event, values = window.read()
        if event == '__TITLEBAR CLOSE__7':
            break
        elif event in 'Logout':
            window['-HOME-'].update(visible=False)
            login_window(window)
    window.close()
    exit(0)


def make_window():
    sg.theme('LightGreen')
    sg.Titlebar(title='Green Foot Forward')

    login_layout = [[sg.Titlebar('Green Foot Forward')],
                    [sg.Text('Welcome to Green Foot Forward!')],
                    [sg.Text('Username:', size=(12, 1)), sg.InputText(key='-USER-', size=(15, 1), do_not_clear=False)],
                    [sg.Text('Password:', size=(12, 1)), sg.InputText(key='-PASS-', size=(15, 1), do_not_clear=False)],
                    [sg.Button('Login'), sg.Button('Create New User')]]

    create_user_layout = [[sg.Titlebar('Create New User')],
                          [sg.Text('Username:', size=(19, 1)),
                           sg.InputText(key='-NEW USER-', size=(15, 1), do_not_clear=False)],
                          [sg.Text('Password:', size=(19, 1)),
                           sg.InputText(key='-NEW PASS-', size=(15, 1), do_not_clear=False)],
                          [sg.Text('Confirm Password:', size=(19, 1)),
                           sg.InputText(key='-PASS_CONF-', size=(15, 1), do_not_clear=False)],
                          [sg.Button('Create'), sg.Button('Cancel')]]

    home_layout = [[sg.Titlebar('Green Foot Forward')],
                   [sg.Text('Main menu')],
                   [sg.Button('Logout')]]

    layouts = [[sg.Column(login_layout, key='-LOGIN-', visible=False),
                sg.Column(create_user_layout, key='-CREATE-', visible=False),
                sg.Column(home_layout, key='-HOME-', visible=False)]]

    window = sg.Window('Green Foot Forward', layouts, grab_anywhere=True, resizable=True, finalize=True)

    return window


def init():
    login_window(make_window())


init()

