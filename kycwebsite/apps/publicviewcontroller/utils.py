def get_project_obj(project):
    return {
        "NAME": project.project_name,
        "IMAGE": project.image_url,
        "VOLUNTEERS": project.members_attended,
        "DATE": f"{project.date.month}/{project.date.day}/{str(project.date.year)[2:]}"
    }


def get_context(request, page_name):
    login_name = 'Login'
    if request.user.is_authenticated:
        login_name = request.user

    return {
        "page_name": page_name,
        "login_name": login_name
    }
