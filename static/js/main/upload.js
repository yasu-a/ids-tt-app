"use strict";

const FILE_UPLOAD_SELECTOR = "#file-upload";
const FORM_UPLOAD_SELECTOR = "form#fileupload";


function generateEntriesHTML(mappings, mappers) {
    let entries_string = $.map(
        mappings,
        (mapping) => {
            let column_strings = $.map(
                mapping,
                (value, key) => {
                    let mapped_value = (mappers[key] || (x => x))(value);
                    return `<div class="column ${key}"><p>${mapped_value}</p></div>`;
                }
            );
            let entry_content = Array.from(column_strings).join("");
            return `<div class="entry">${entry_content}</div>`;
        }
    );
    return Array.from(entries_string).join("");
}

let filesToBeUploaded = [];

function pushFiles(files) {
    $.each(
        files,
        (index, file) => filesToBeUploaded.push(file)
    )
}

function updateFileList() {
    let content = generateEntriesHTML(
        $.map(
            filesToBeUploaded,
            (file) => {
                return {
                    name: file.name,
                    size: file.size,
                    datetime: file.lastModifiedDate
                };
            }
        ),
        {
            size: value => `${Math.floor(value / 1000)} KB`,
            datetime: value => `${value.toISOString().slice(0, 10)} ${value.toISOString().slice(11, 19)}`
        }
    );
    $(".file-list").html(content);
}

function uploadFile(file) {
    const fd = new FormData();
    fd.append("file", file, file.name);
    fd.append("upload_file", true);

    $.ajax({
        type: "POST",
        url: "{{ url_for(\".post_upload\") }}",
        async: true,
        data: fd,
        cache: false,
        contentType: "multipart/form-data",
        processData: false,
        timeout: 60000
    }).done((result) => {
        console.log(result);
    }).fail((result) => {
        console.log(result);
    });
}

$("document").ready(() => {
    $(FILE_UPLOAD_SELECTOR).change((evt) => {
        let files = $(FILE_UPLOAD_SELECTOR).prop("files");
        pushFiles(files);
        updateFileList();
    });
    $(FORM_UPLOAD_SELECTOR).submit((evt) => {
        evt.preventDefault();
        console.log(evt);
        $.each(
            filesToBeUploaded,
            (file) => {
                console.log(file);
                uploadFile(file);
            }
        );
    });
});