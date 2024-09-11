import flet as ft
from flet import colors
from pymongo import MongoClient
import functools
import threading
import time

def main(page: ft.Page):
    page.title = "KDPWCCP App"
    page.bgcolor = colors.BLACK

    client = MongoClient("mongodb+srv://moiz121:test123456@cluster0.lq8grwq.mongodb.net/")  
    db = client["UserAuthDB"]
    users_collection = db["Users"]

    navigation_stack = []

    def show_message(message, success=True):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=colors.GREEN if success else colors.RED
        )
        page.snack_bar.open = True
        page.update()

    documents = []

    def preload_data(callback=None):
        global documents
        client = MongoClient("mongodb+srv://moiz121:test123456@cluster0.lq8grwq.mongodb.net/")
        db = client["KDPWCCP"]
        collection = db["RefineddataOrganizedMarket"]
        documents = list(collection.find())
        print(f"Loaded {len(documents)} documents.")
        if callback:
            callback()

    def navigate_to(route, clear_history=False):
        if clear_history:
            navigation_stack.clear()
        navigation_stack.append(route)
        route_change(route)

    def go_back(e):
        if len(navigation_stack) > 1:
            navigation_stack.pop()
            previous_route = navigation_stack[-1]
            route_change(previous_route)
        else:
            show_message("You're already at the main page", success=False)

    def route_change(route):
        page.controls.clear()
        
        # Reseting page properties for each route change
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.scroll = None

        if route == "/":
            load_main_page()
        elif route == "/login":
            load_Login_page()
        elif route == "/signup":
            load_Signup_page()
        elif route == "/circulars":
            load_circulars_page()
        elif route == "/otc_circulars":
            load_OTCcirculars_page()
        page.update()

    def open_pdf(e, link):
        if link:
            try:
                page.launch_url(link)
            except Exception as ex:
                print(f"Failed to open PDF link: {ex}")
                show_message("Failed to open PDF. Please try again later.", success=False)
        else:
            print("Invalid PDF link")
            show_message("Invalid PDF link.", success=False) 

    def handle_login(e):
        username = username_field.value.strip()
        password = password_field.value.strip()

        if not username or not password:
            show_message("Username and password cannot be empty!", success=False)
        else:
            user = users_collection.find_one({"username": username})
            if user and user["password"] == password:
                show_message("Login successful!", success=True)

                page.controls.clear()
                pr = ft.ProgressRing()

                page.add(
                    ft.Row(
                        [
                            pr,
                            ft.Text("Wait for the completion...", size=16, weight="bold", color="WHITE")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    )
                )

                page.update()
                threading.Thread(target=preload_data, args=(lambda: navigate_to("/circulars"),)).start()
            else:
                show_message("Invalid username or password.", success=False)

    def handle_signup(e):
        username = signup_username_field.value.strip()
        password = signup_password_field.value.strip()
        confirm_password = signup_confirm_password_field.value.strip()

        if not username or not password or not confirm_password:
            show_message("All fields must be filled out!", success=False)
        elif password != confirm_password:
            show_message("Passwords do not match.", success=False)
        else:
            if users_collection.find_one({"username": username}):
                show_message("Username already exists.", success=False)
            else:
                users_collection.insert_one({"username": username, "password": password})
                show_message("Signup successful!", success=True)
                navigate_to("/login")

    def load_Login_page():
        global username_field, password_field

        username_field = ft.TextField(label="Username", color="white", autofocus=True, border_color=colors.YELLOW, border_radius=28)
        password_field = ft.TextField(label="Password", color="white", border_color=colors.YELLOW, password=True, can_reveal_password=True, border_radius=28)

        page.add(
            ft.Column(
                [
                    ft.Image(
                        src="https://cdn-icons-png.flaticon.com/128/295/295128.png",
                        width=100,
                        height=100,
                        fit=ft.ImageFit.COVER
                    ),
                    ft.Text("LOGIN", size=30, weight="bold", text_align="center", color="WHITE"),
                    username_field,
                    password_field,
                    ft.ElevatedButton(text="Log In", bgcolor=colors.YELLOW, color=colors.BLACK, on_click=handle_login, width=500),
                    ft.Text("Don't have an account?", size=12, weight="bold", text_align="center", color="WHITE"),
                    ft.ElevatedButton(text="Sign Up", bgcolor=colors.GREEN, color=colors.WHITE, on_click=lambda _: navigate_to("/signup"), width=300),
                    ft.ElevatedButton(text="Back to Main", bgcolor=colors.RED, color=colors.WHITE, on_click=lambda _: navigate_to("/"))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )

    def load_Signup_page():
        global signup_username_field, signup_password_field, signup_confirm_password_field

        signup_username_field = ft.TextField(label="Username", color="white", autofocus=True, border_color=colors.YELLOW, border_radius=28)
        signup_password_field = ft.TextField(label="Password", color="white", border_color=colors.YELLOW, password=True, can_reveal_password=True, border_radius=28)
        signup_confirm_password_field = ft.TextField(label="Confirm Password", color="white", border_color=colors.YELLOW, password=True, can_reveal_password=True, border_radius=28)

        page.add(
            ft.Column(
                [
                    ft.Image(
                        src="https://cdn-icons-png.flaticon.com/128/15753/15753940.png",
                        width=90,
                        height=90,
                        fit=ft.ImageFit.COVER
                    ),
                    ft.Text("SIGNUP", size=30, weight="bold", text_align="center", color="WHITE"),
                    signup_username_field,
                    signup_password_field,
                    signup_confirm_password_field,
                    ft.ElevatedButton(text="Sign Up", bgcolor=colors.YELLOW, color=colors.BLACK, on_click=handle_signup, width=500),
                    ft.Text("Already have an account?", size=12, weight="bold", text_align="center", color="WHITE"),
                    ft.ElevatedButton(text="Back to Login", bgcolor=colors.RED, color=colors.WHITE, on_click=lambda _: navigate_to("/login"))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )

    def setup_header(title):
        return ft.Row(
            [
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    icon_size=24,
                    on_click=go_back,
                ),
                ft.Container(
                    content=ft.Text(
                        title, 
                        size=30, 
                        weight="bold", 
                        text_align="center", 
                        color="WHITE"
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                ),
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        )

    def setup_buttons():
        return ft.Row(
            [
                ft.ElevatedButton(text="Organized Market"),
                ft.ElevatedButton(
                    text="OTC",
                    on_click=lambda _: navigate_to("/otc_circulars")
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        )

    def setup_list_view(documents):
        return ft.ListView(
            controls=[
                ft.Container(  
                    content=ft.Column(
                        [
                            ft.Text(doc.get('resolution_number', 'N/A'), size=20, weight="bold", color="WHITE"),
                            ft.Text(doc.get('resolution_detail', 'No details available'), size=12, color="WHITE"),
                            ft.Text(f"Launch Date: {doc.get('launch_date', 'N/A')}", size=12, color="WHITE"),
                            ft.Text(f"Summary: {doc.get('AI_summary_of_PDF', 'No summary available')}", size=12, color="WHITE"),
                            ft.ElevatedButton(
                                text="View PDF", 
                                bgcolor=colors.YELLOW, 
                                color=colors.BLACK,
                                on_click=functools.partial(open_pdf, link=doc.get('pdf_link', ''))
                            ),
                        ]
                    ),
                    bgcolor=colors.BLUE,
                    padding=ft.padding.all(10),
                    border_radius=8,
                    margin=ft.margin.all(10),
                    shadow=ft.BoxShadow(
                        color=colors.BLACK,
                        blur_radius=10,
                        spread_radius=2,
                        offset=ft.Offset(0, 2),
                    ),
                )
                for doc in documents
            ],
            spacing=10,
            padding=ft.padding.all(10),
            auto_scroll=True,
        )

    def load_circulars_page():
        client = MongoClient("mongodb+srv://moiz121:test123456@cluster0.lq8grwq.mongodb.net/")
        db = client["KDPWCCP"]
        collection = db["RefineddataOrganizedMarket"]
        documents = collection.find()

        page.scroll = "auto"
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.add(
            ft.Column(
                [
                    setup_header("Find Resolutions"),
                    setup_buttons(),
                    setup_list_view(documents),
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
            )
        )

    def load_OTCcirculars_page():
        client = MongoClient("mongodb+srv://moiz121:test123456@cluster0.lq8grwq.mongodb.net/")
        db = client["KDPWCCP"]
        collection = db["RefineddataOTC"]
        documents = collection.find()

        page.scroll = "auto"
        page.horizontal_alignment = ft.CrossAxisAlignment.START
        page.vertical_alignment = ft.MainAxisAlignment.START
        page.add(
            ft.Column(
                [
                    setup_header("Resolutions OTC"),
                    setup_buttons(),
                    setup_list_view(documents),
                ],
                alignment=ft.MainAxisAlignment.START,
                expand=True,
            )
        )

    def load_main_page():
        page.add(
            ft.Column(
                [
                    ft.Image(
                        src="https://cdn-icons-png.flaticon.com/128/9555/9555155.png",
                        width=200,
                        height=200,
                        fit=ft.ImageFit.COVER
                    ),
                    ft.Text("KDPWCCP", size=63, weight="bold", text_align="center", color="WHITE"),
                    ft.Text("Securing financial transactions with trusted expertise.", size=12, weight="bold", text_align="center", color="WHITE"),
                    ft.ElevatedButton(text="CONTINUE", bgcolor=colors.YELLOW, color=colors.BLACK, on_click=lambda _: navigate_to("/login")),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )

   
    navigate_to("/", clear_history=True)

ft.app(target=main, view=ft.WEB_BROWSER)