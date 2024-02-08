$(document).ready(function () {
    $("#categorySwitch").change(function () {
        if (this.checked) {
            $("#category-input").show();
            $(".category-checkbox").hide();
        } else {
            $("#category-input").hide();
            $(".category-checkbox").show();
        }
    });
});

function checkAndDisplayLink(noteSource) {
    if (/^https?:\/\//.test(noteSource)) {
        document.write('<a href="' + noteSource + '">' + noteSource + '</a>');
    } else {
        document.write(noteSource);
    }
}

$(document).ready(function(){
    $("#myInput").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#myTable tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });

jQuery(document).ready(function($) {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });
});



function downloadCSV() {
    var searchCriteria = document.getElementById('myInput').value;

    var xhr = new XMLHttpRequest();
    xhr.open('GET', "/export-all-notes-csv?search_criteria=" + encodeURIComponent(searchCriteria), true);
    xhr.responseType = 'blob';

    xhr.onload = function() {
        var blob = new Blob([xhr.response], { type: 'text/csv' });
        var link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = 'filtered_notes_export.csv';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    xhr.send();
}


function exportNoteToCSV() {
    var note_id = "{{ note_id }}";  // Replace this with the correct variable holding note_id

    // Show loading indicator
    document.getElementById('exportLoading').style.display = 'inline';

    var xhr = new XMLHttpRequest();
    xhr.open('GET', "{{ url_for('export_note_csv', note_id=note_id) }}", true);
    xhr.responseType = 'blob';

    xhr.onload = function () {
        // Hide loading indicator
        document.getElementById('exportLoading').style.display = 'none';

        var blob = new Blob([xhr.response], {type: 'text/csv'});
        var link = document.createElement('a');
        link.href = window.URL.createObjectURL(blob);
        link.download = 'export_note_csv';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    xhr.send();
}

function waarschuwing_met_uitloggen() {

    var waarschuwing_met_uitloggen = confirm("Weet u zeker dat u uit wilt loggen?");
    if (waarschuwing_met_uitloggen) {
        window.location.href = "http://127.0.0.1:5000/";
    } else {
    // blijf op dezelfde pagina (er gebeurt niks)
    }
}

//Live filtering functie
$(document).ready(function () {

    $('#publicSwitchFilter').change(function () {
        updateTable();
    });

    $('#teacherSwitchFilter').change(function () {
        updateTable();
    });

    function updateTable() {
        var publicSwitchFilter = $('#publicSwitchFilter').prop('checked') ? 'on' : 'off';
        var teacherSwitchFilter = $('#teacherSwitchFilter').prop('checked') ? 'on' : 'off';

        $.ajax({
            type: 'POST',
            url: '/notes-overview', 
            data: {
                publicSwitchFilter: publicSwitchFilter,
                teacherSwitchFilter: teacherSwitchFilter 
            },
            success: function (data) {

                var newTbodyContent = $(data).find('tbody').html();
        
                if (!newTbodyContent) {
                    newTbodyContent = $(data).html();
                }
        
                $('tbody').html(newTbodyContent);
        
                $('tbody tr').addClass('clickable-row').each(function () {
                    var noteId = $(this).data('note-id');
                    $(this).attr('data-href', "{{ url_for('view_note', note_id=" + noteId + ") }}");
                });
            },
            error: function (error) {
                console.log(error);
            }
        });
    }
});