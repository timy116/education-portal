function disableOnClick(id) {
  return () => {
    $(id).attr('disabled', true)

    return true
  }
}

function studentsCsvChange(targetId) {
  return function () {
    $(this).parse({
      config: {
        header: true,
        transformHeader(header) {
          return header.toLowerCase()
        },
        complete(results) {
          if (!results.meta.fields.includes('name'))
            return alert(`在 CSV 檔裡面找不到欄位 'name'。`)

          const newStudents = results.data.map((row) => row['name']).join('\n')
          const curStudents = $(targetId).val()
          $(targetId).val(`${newStudents}\n${curStudents}`)
        },
        skipEmptyLines: true,
      }
    })
  }
}

function importStudentsFromCSV(triggerId, targetId) {
  $(triggerId).on('click', () => {
    const fileInput = $('<input>').attr({
      type: 'file',
      accept: 'text/csv',
    })

    fileInput.on('change', studentsCsvChange(targetId))
    fileInput.trigger('click')
  })
}
