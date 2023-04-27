"use strict";


const validators = {
    "uid": ($input) => {
        const value = $input.val();

        if (value === "") {
            return "Enter name";
        }
    },
    "mail": ($input) => {
        const value = $input.val();

        if (value === "") {
            return "Enter e-mail address";
        }
    },
    "pw": ($input) => {
        const value = $input.val();

        if (value === "") {
            return "Enter password";
        } else if (value.length < 8) {
            return "Password is too short";
        }

    },
    "pw-confirm": ($input) => {
        const value = $input.val();

        if (value === "") {
            return "Enter password";
        } else if (value !== $("input[name='pw']").val()) {
            return "Passwords do not match";
        }
    }
}

function validate_input($input) {
    const name = $input.attr("name");
    const validator = validators[name];

    let result = validator($input);
    if (result === undefined) {
        result = "";
    }
    $input.siblings().find(".item-message").text(result);

    const map_result = $("#form-create-account .input-item .item-message").map(
        (_, element) => {
            return $(element).text() !== "";
        }
    );
    const enable_submission = $.grep(map_result, (x) => x).length === 0;
    $("#button-submit").prop("disabled", !enable_submission);
}

function validate_all() {
    $("#form-create-account input").each(
        (_, element) => {
            validate_input($(element));
        }
    );
}

$(document).on("keyup", "#form-create-account input", (evt) => {
    validate_all();
});


$(document).ready(
    () => {
        validate_all();
    }
);