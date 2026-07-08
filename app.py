import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Todo App", page_icon="✅", layout="centered")
st.title("✅ Todo App")


# ---------- API Helpers ----------

def get_all_todos():
    try:
        res = requests.get(f"{API_URL}/todos")
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to FastAPI server.\n{e}")
        return None


def create_todo(todo_id, title, is_completed):
    try:
        return requests.post(
            f"{API_URL}/todos",
            json={
                "id": todo_id,
                "title": title,
                "isCompleted": is_completed,
            },
        )
    except requests.exceptions.RequestException as e:
        st.error(e)
        return None


def update_todo(todo_id, title, is_completed):
    try:
        return requests.put(
            f"{API_URL}/todos/{todo_id}",
            json={
                "id": todo_id,
                "title": title,
                "isCompleted": is_completed,
            },
        )
    except requests.exceptions.RequestException as e:
        st.error(e)
        return None


def delete_todo(todo_id):
    try:
        return requests.delete(f"{API_URL}/todos/{todo_id}")
    except requests.exceptions.RequestException as e:
        st.error(e)
        return None


# ---------- Load Todos ----------

todos = get_all_todos()

if todos is None:
    st.stop()


# ---------- Create Todo ----------

st.subheader("➕ Add Todo")

with st.form("create_form", clear_on_submit=True):

    new_id = st.number_input("ID", min_value=1, step=1)

    new_title = st.text_input("Title")

    new_completed = st.checkbox("Completed")

    submitted = st.form_submit_button("Add Todo")

    if submitted:

        if not new_title.strip():
            st.warning("Title cannot be empty.")

        elif any(todo.get("id") == int(new_id) for todo in todos):
            st.warning("ID already exists.")

        else:
            res = create_todo(
                int(new_id),
                new_title.strip(),
                new_completed,
            )

            if res and res.ok:
                st.success("Todo created successfully!")
                st.rerun()
            else:
                st.error("Failed to create todo.")


st.divider()

# ---------- Display Todos ----------

st.subheader("📋 Your Todos")

if len(todos) == 0:
    st.info("No todos available.")

else:

    for todo in todos:

        todo_id = todo.get("id")

        with st.container(border=True):

            col1, col2, col3 = st.columns([6, 1, 1])

            with col1:

                checked = st.checkbox(
                    todo.get("title", ""),
                    value=todo.get("isCompleted", False),
                    key=f"check_{todo_id}",
                )

                if checked != todo.get("isCompleted", False):

                    res = update_todo(
                        todo_id,
                        todo.get("title", ""),
                        checked,
                    )

                    if res and res.ok:
                        st.rerun()
                    else:
                        st.error("Failed to update status.")

            with col2:

                if st.button("✏️", key=f"edit_{todo_id}"):

                    st.session_state[f"editing_{todo_id}"] = True

            with col3:

                if st.button("🗑️", key=f"delete_{todo_id}"):

                    res = delete_todo(todo_id)

                    if res and res.ok:
                        st.success("Deleted!")
                        st.rerun()
                    else:
                        st.error("Delete failed.")

            if st.session_state.get(f"editing_{todo_id}", False):

                with st.form(f"edit_form_{todo_id}"):

                    edited_title = st.text_input(
                        "Title",
                        value=todo.get("title", ""),
                    )

                    edited_completed = st.checkbox(
                        "Completed",
                        value=todo.get("isCompleted", False),
                    )

                    col_save, col_cancel = st.columns(2)

                    with col_save:
                        save = st.form_submit_button("Save")

                    with col_cancel:
                        cancel = st.form_submit_button("Cancel")

                    if save:

                        if not edited_title.strip():
                            st.warning("Title cannot be empty.")

                        else:

                            res = update_todo(
                                todo_id,
                                edited_title.strip(),
                                edited_completed,
                            )

                            if res and res.ok:
                                st.session_state[f"editing_{todo_id}"] = False
                                st.success("Updated!")
                                st.rerun()
                            else:
                                st.error("Update failed.")

                    if cancel:
                        st.session_state[f"editing_{todo_id}"] = False
                        st.rerun()


st.divider()

if st.button("🔄 Refresh"):
    st.rerun()