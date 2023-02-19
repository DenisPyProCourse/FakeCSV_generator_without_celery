$(document).ready(() => {
   console.log('Status Check!');
});

$('.btn').on('click', function () {
    $.ajax({
        url: '/schemas/tasks/',
        data: {ds: $(this).data('type'), rows: $('#id_rows').val() },
        method: 'POST',
    })
        .done(() => {
            // getStatus();
            $(document).ready(() => {
   $('#tasks').text("Processing").css({
    'color': 'Blue'
})});
        })
        .fail((err) => {
            console.log(err);
        });
});

// function getStatus() {
//     $.ajax({
//         url: `/schemas/tasks/`,
//         method: 'GET'
//     })
//     // .done((res) => {
//         .$('#tasks').text("Processing").css({
//     'color': 'Blue'
//   });
//
//
//             // const taskStatus = res.task_status;
//             //
//             // if (taskStatus === 'SUCCESS') return false;
//             // if (taskStatus === 'FAILURE'){
//             //     $(document).ready(() => {
//             //        $('#tasks').text("Error").css({
//             //         'color': 'red'
//             //     })});
//             // }
//             setTimeout(function () {
//                 getStatus(res);
//             }, 1000);

        // }
        //
        // .fail((err) => {
        //     console.log(err)
        // });

$(document).ready(() => {
   $('#tasks').text("Ready").css({
    'color': 'green'
})});
