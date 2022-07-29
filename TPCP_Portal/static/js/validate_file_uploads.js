

function ensure_file_to_load() {


    let files = document.forms["upload_files"]["files[]"].value;
    console.log(files);
    if (!files){
        event.preventDefault();
//        alert("Validation Failed");
        document.getElementById("upload_section").classList.add("error-on-input-field");

        document.getElementById("file_upload_error_text").classList.remove("do-not-display");
        document.getElementById("file_upload_error_text").classList.add("do-display");

        return false;
    }

    return true;
}

