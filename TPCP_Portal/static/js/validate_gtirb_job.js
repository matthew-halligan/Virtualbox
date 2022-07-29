function validate_gtirb_job(job_id){
//  Information for validation
    let JobInfoFormID = "JobInfoForm" + job_id;
    let transform_set = document.forms[JobInfoFormID]["JobTransform"].value;
    let metric_collection = document.forms[JobInfoFormID]["JobMetrics"].value;

//  Transformation Items
    let transform_section_id = "job_transform_section_" + job_id;
    let transform_text_id = "job_transform_must_select_" + job_id

//  Metrics Items
    let metrics_section_id = "job_metrics_section_" + job_id;
    let metrics_text_id = "job_metrics_must_select_" + job_id

    let __flag = "not tripped";
    if (transform_set == "Must Select"){

        __flag = "tripped";
        document.getElementById(transform_text_id).classList.remove("do-not-display");
        document.getElementById(transform_text_id).classList.add("do-display");

        document.getElementById(transform_section_id).classList.add("error-on-input-field");

    }
    if (metric_collection == "Must Select"){

        __flag = "tripped";
        document.getElementById(metrics_text_id).classList.remove("do-not-display");
        document.getElementById(metrics_text_id).classList.add("do-display");

        document.getElementById(metrics_section_id).classList.add("error-on-input-field");

    }

    if (__flag != "tripped"){
        return true;
    }
    event.preventDefault();
    return false;
}