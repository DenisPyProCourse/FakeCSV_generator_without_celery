$(document).ready(() => {
   console.log('Status Check!');
});

$('.btn').on('click', function () {
    $.ajax({
        url: '/schemas/tasks/',
        // data: { rows: $(this).data('type'), pk: $(this).data('type2') },
        data: {ds: $(this).data('type'), rows: $('#id_rows').val() },
        // data: {ds: $('#data-type').innerText},
        method: 'POST',
    })
        .done((res) => {
            getStatus(res.task_id);
        })
        .fail((err) => {
            console.log(err);
        });
});

function getStatus(taskId) {
    $.ajax({
        url: `/schemas/tasks/${taskId}/`,
        method: 'GET'
    })
    .done((res) => {
                    $('#tasks').text("Processing").css({
    'color': 'Blue'
  });


            const taskStatus = res.task_status;

            if (taskStatus === 'SUCCESS') return false;
            if (taskStatus === 'FAILURE'){
                $(document).ready(() => {
                   $('#tasks').text("Error").css({
                    'color': 'red'
                })});
            }
            setTimeout(function () {
                getStatus(res.task_id);
            }, 1000);

        })

        .fail((err) => {
            console.log(err)
        });
}
$(document).ready(() => {
   $('#tasks').text("Ready").css({
    'color': 'green'
})});
