import reflex as rx

from autoapply_ai.state import State
from autoapply_ai.components.layout import layout


def profile() -> rx.Component:
    return layout(
        rx.vstack(

            rx.heading("Profile"),

            rx.input(
                placeholder="Your Name",
                value=State.profile_name,
                on_change=State.set_profile_name,
            ),

            rx.input(
                placeholder="Headline",
                value=State.headline,
                on_change=State.set_headline,
            ),

            rx.input(
                placeholder="Location",
                value=State.location,
                on_change=State.set_location,
            ),

            rx.text_area(
                placeholder="About Me",
                value=State.bio,
                on_change=State.set_bio,
            ),

            rx.input(
                placeholder="Skills",
                value=State.skills,
                on_change=State.set_skills,
            ),

            rx.input(
                placeholder="Education",
                value=State.education,
                on_change=State.set_education,
            ),

            rx.input(
                placeholder="Experience",
                value=State.experience,
                on_change=State.set_experience,
            ),

            rx.input(
                placeholder="GitHub URL",
                value=State.github_url,
                on_change=State.set_github_url,
            ),

            rx.input(
                placeholder="LinkedIn URL",
                value=State.linkedin_url,
                on_change=State.set_linkedin_url,
            ),

            rx.button(
                "Save Profile",
                on_click=State.save_profile,
            ),

            spacing="4",
            width="100%",
        )
    )