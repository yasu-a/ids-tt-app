"use strict";

const FILE_UPLOAD_SELECTOR = "#file-upload";

const CSV_ICON = "<img src=\"data:image/svg+xml;base64,PHN2ZyBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGZpbGwtcnVsZT0iZXZlbm9kZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgc3Ryb2tlLW1pdGVybGltaXQ9IjIiIHZpZXdCb3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBkPSJtMjEgNGMwLS40NzgtLjM3OS0xLTEtMWgtMTZjLS42MiAwLTEgLjUxOS0xIDF2MTZjMCAuNjIxLjUyIDEgMSAxaDE2Yy40NzggMCAxLS4zNzkgMS0xem0tMTYuNS41aDE1djE1aC0xNXptMTIuNSAxMC43NWMwLS40MTQtLjMzNi0uNzUtLjc1LS43NWgtOC41Yy0uNDE0IDAtLjc1LjMzNi0uNzUuNzVzLjMzNi43NS43NS43NWg4LjVjLjQxNCAwIC43NS0uMzM2Ljc1LS43NXptMC0zLjI0OGMwLS40MTQtLjMzNi0uNzUtLjc1LS43NWgtOC41Yy0uNDE0IDAtLjc1LjMzNi0uNzUuNzVzLjMzNi43NS43NS43NWg4LjVjLjQxNCAwIC43NS0uMzM2Ljc1LS43NXptMC0zLjI1MmMwLS40MTQtLjMzNi0uNzUtLjc1LS43NWgtOC41Yy0uNDE0IDAtLjc1LjMzNi0uNzUuNzVzLjMzNi43NS43NS43NWg4LjVjLjQxNCAwIC43NS0uMzM2Ljc1LS43NXoiIGZpbGwtcnVsZT0ibm9uemVybyIvPjwvc3ZnPg==\">";


function generateEntriesHTML(mappings, mappers) {
    let entries_string = $.map(
        mappings,
        mapping => {
            console.log(Object.entries(mapping));
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
    let content_string = Array.from(entries_string).join("");
    console.log(content_string);
    return content_string;
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
    console.log(content);
    $(".file-list").html(content);
}

$("document").ready(() => {
    $(FILE_UPLOAD_SELECTOR).change(
        (evt) => {
            let files = $(FILE_UPLOAD_SELECTOR).prop("files");
            pushFiles(files);
            updateFileList();
        }
    );
});