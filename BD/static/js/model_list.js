{
let neighborhoodIdFields = document.querySelectorAll('[name="neighborhood_id"]');//Подсказка при наведении на номер участка у доктора
sendData({},null,null,"POST","/get_str_neigh_dict/")
.then(response => {
    let streetDict = response;
    neighborhoodIdFields.forEach(element => {
    element.setAttribute('title', streetDict[element.textContent]);})
})
}

{//Проверка прав для удаления
    if (user_group != "Пациенты")
    {
        let user_perm_arr_BD = user_perm.split(", ");
        let user_perm_arr = user_perm_arr_BD.map(item => item.split('.')[1]);
        model_dict = {
            "Участки":"neighborhood",
            "Пациенты":"patient",
            "Цели визита":"visit",
            "Врачи":"doctor",
            "Талоны":"ticket",
            "Диагнозы":"diagnosis"}
        if (user_perm.includes("delete_"+model_dict[model]))  {EnableDelete();}
    }
}


function MakePatientDiagnosis(e,element,new_td,id,type,IsTextId,TextIdFunc,IdFunc)
{
    let selectedText = e.params.data.text;
        if (IsTextId)
        {
            let selectedValue = e.params.data.id;
        } else
        {
        }
}

{
sendData({"field_name":"diagnosis","model_name":"Диагнозы"},null,null,"POST", "/get_fields_by_name/")
    .then(response => {
        let patientLink = document.querySelector('[name="patient_list"]');
        patientLink.addEventListener('click', function() {
        createDropdown(patientLink,response.values,response.type,null,null,MakePatientDiagnosis,'div')
        })
});
}


function ListForEdit(e,element,new_td,id,type,IsTextId,TextIdFunc,IdFunc)//[]функция для поведения - что будет если выбрать элемент в списке
{
    let selectedText = e.params.data.text;
        if (IsTextId)
        {
            let selectedValue = e.params.data.id;
            TextIdFunc(type,selectedValue,id,element,selectedText,new_td)// Запрос валидацию внешних ключей,статуса/изменения в бд
            .then(response =>
            {
                if (response.key !== undefined)
                {
                    new_row[response.key]=response.value;
                       if (fields == Object.keys(new_row).length)
                    {
                        sendData({...new_row,...{"model_name":model}},element,element,"POST","/row_add/");
                        new_row = {}
                        location.reload();
                    }
                }

            }
            )
            .catch(error => {
            console.error("Ошибка", error);
            });
        } else
        {
            IdFunc(type,id,element,selectedText,new_td)// Запрос валидацию внешних ключей,статуса/изменения в бд
            .then(response =>
            {
             if (response.key !== undefined)
                {
                    new_row[response.key]=response.value;
                        if (fields == Object.keys(new_row).length)
                    {
                        sendData({...new_row,...{"model_name":model}},element,element,"POST","/row_add/");
                        new_row = {}
                        location.reload();
                    }
                }
            }
            )
            .catch(error => {
            console.error("Ошибка", error);
            });
        }
}

function EnableDelete()
{
    let cells = document.querySelectorAll('tr');
    cells.forEach(cell => {
        if (cell.parentElement.tagName != 'THEAD')
        {
            let emptyCell = document.createElement('td');
            let closeButton = document.createElement('button');
            closeButton.classList.add('close-btn');
            closeButton.innerHTML = '×';
            cell.appendChild(emptyCell);
            emptyCell.appendChild(closeButton);
        }
        else{
        let emptyCell = document.createElement('td');
        cell.appendChild(emptyCell);
        }
    });
    const buttons = document.querySelectorAll('.close-btn');
    buttons.forEach(button => {
        button.addEventListener('click', () => {
            showConfirm(`Вы хотите удалить элемент с номером ${button.parentElement.parentElement.children[0].innerHTML} ?`, function (result) {
            if (result) {
                sendData({"id":button.parentElement.parentElement.children[0].innerHTML,"model_name":model},button,button,"POST","/row_delete/");
                setTimeout(() => { location.reload(); }, 500);
            }
            });
        });
    });
}

function showConfirm(message, callback) {
    let html = document.querySelector('html');
    let modal = document.createElement('div');
    modal.setAttribute('id','customConfirm');
    modal.setAttribute('class','modal_wind');
    let modal_content = document.createElement('div');
    modal_content.setAttribute('class','modal-content');
    let yesButton = document.createElement('button');
    yesButton.setAttribute('id','confirmYes');
    yesButton.setAttribute('class','btn_modal');
    yesButton.innerHTML = '✔';
    let noButton = document.createElement('button');
    noButton.innerHTML = '✖';
    noButton.setAttribute('id','confirmNo');
    noButton.setAttribute('class','btn_modal');
    let paragraph = document.createElement('p');
    paragraph.textContent = message;
    html.appendChild(modal);
    modal.appendChild(modal_content);
    modal_content.appendChild(yesButton);
    modal_content.appendChild(noButton);
    modal_content.appendChild(paragraph);
    modal.style.display = 'block';
    yesButton.onclick = function () {
        modal.style.display = 'none'; // Закрыть окно
        callback(true); // Возвращаем "Да"
    };
    noButton.onclick = function () {
        modal.style.display = 'none'; // Закрыть окно
        callback(false); // Возвращаем "Нет"
    };
}

function getCsrfToken() {
  let match = document.cookie.split('csrftoken=')[1];
  if (match) return match;
  return null;
}
function makeEditable(element) {//при клике на ячейку она становится редактируемой/появл-ся список значений
    if (user_group != "Пациенты")
    {
        let user_perm_arr_BD = user_perm.split(", ");
        let user_perm_arr = user_perm_arr_BD.map(item => item.split('.')[1]);
        model_dict = {
            "Участки":"neighborhood",
            "Пациенты":"patient",
            "Цели визита":"visit",
            "Врачи":"doctor",
            "Талоны":"ticket",
            "Диагнозы":"diagnosis"}
        if (user_perm.includes("change_"+model_dict[model]))
        {
            let list_fields = ["category","status","street","neighborhood_id","visit_id","diagnosis_id","doctor_id","patient_id"];
            last_data = element.innerText;
            field = element.getAttribute("Name");
            if (list_fields.includes(field))//Если ячейка имеет тип данных - перечисление
            {
                element.focus();
                sendData({"field_name":field,"model_name":model},element,element,"POST", "/get_fields_by_name/")
                .then(response => {
                createDropdown(element,response.values,response.type,
                (type,selectedValue,id,element,selectedText,new_element)=>{return sendData({"type":type,"field_id":selectedValue,"id":id,"model_name":model,"field_name":element.getAttribute('name'),"last_data":element.innerText,"new_data":selectedText},element,new_element,"POST","/change_by_list/")},
                (type,id,element,selectedText,new_element)=>{return sendData({"type":type,"id":id,"model_name":model,"field_name":element.getAttribute('name'),"last_data":element.innerText,"new_data":selectedText},element,new_element,"POST","/change_by_list/")},//то создаётся выпадающий список
                ListForEdit,'td')})
                .catch(error => {
                console.error('Ошибка: ', error);
                });
                return
            }
            element.contentEditable = true;
            element.focus();
            enterIsPressed = false;//нужно т.к при вызове onkeydown вызывается сразу же onblur
            /*при потере фокуса, идёт поиск данной строки в БД,
            идёт попытка присвоить полю новое значение,
            если успешно то записывается,иначе возвращает ошибку*/
            element.onkeydown = (event) => {if (event.key === 'Enter' && !enterIsPressed)  {enterIsPressed=true; requestTextUpdate(event, element);}}
            element.onblur = (event) => {if (!enterIsPressed) {requestTextUpdate(event, element)} enterIsPressed = false;}
        }
    }
}

function requestTextUpdate (event,element)
{
    element.contentEditable = false;
    children = element.parentElement.children;
    index = Array.prototype.indexOf.call(children, element);
    thead = document.querySelector('thead').firstElementChild;
    field_name = thead.children[index].innerText;
    let data = {
      "last_data":last_data,
      "table_verbose_name_plural": model,
      "id": element.parentElement.firstElementChild.innerText,
      "field_name":field_name,
      "new_data":element.innerText,
    };
    sendData(data,element,element,"POST", "/change/")
    .then(response =>
                    {
                        new_row[response.key]=response.value;
                        if (fields == Object.keys(new_row).length)
                        {
                            sendData({...new_row,...{"model_name":model}},element,element,"POST","/row_add/");
                            new_row = {}
                            location.reload();
                        }
                    }
                    )

}
function sendData(data, element,new_element, method, dir) {
    return new Promise((resolve, reject) => {
        csrfToken = getCsrfToken();
        let xhr = new XMLHttpRequest();
        xhr.open(method, dir, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.setRequestHeader("X-CSRFToken", csrfToken);
        let jsonData = JSON.stringify(data);
        xhr.onload = function () {
            let response;
            if (xhr.status == 200) {
                response = JSON.parse(xhr.responseText);
                resolve(response); // Разрешаем промис с данными ответа
            } else {
                if (xhr.status != 304) {
                    response = JSON.parse(xhr.responseText);
                    showPopups(response.response);
                    if (element.getAttribute('data-select2-id')===null)//Если ноль то, это не список
                    {
                        element.classList.add('highlight-error');
                        setTimeout(() => { element.classList.remove('highlight-error'); }, 1000);
                        element.selectedIndex = -1;
                        element.innerText = last_data;
                        reject(response); // Отклоняем промис с ошибкой
                    }
                    element = new_element;
                    try
                    {element = element.children[1].children[0].children[0];}
                    catch(error)
                    {
                        element.classList.add('highlight-error');
                        setTimeout(() => { element.classList.remove('highlight-error'); }, 1000);
                        element.selectedIndex = -1;
                        reject(response); // Отклоняем промис с ошибкой
                    }
                    element.classList.add('highlight-error');
                    setTimeout(() => { element.classList.remove('highlight-error'); }, 1000);
                    reject(response); // Отклоняем промис с ошибкой
                }
            }
        };
        xhr.send(jsonData);
    });
}

function showPopup(text) {//черное уведомление справа
    return new Promise((resolve) => {
        const errorsDiv = document.querySelector('.errors');
        const popup = document.createElement('div');
        popup.setAttribute('id', 'popup');
        popup.innerText = text;
        popup.style.display = "flex";
        popup.style.opacity = "1";
        errorsDiv.appendChild(popup);
        setTimeout(() => {
            popup.style.transition = "opacity 1s";
            popup.style.opacity = "0";
        }, 2000);
        setTimeout(() => {
            popup.remove();
            resolve();
        }, 3000);
    });
}

async function showPopups(text) {await showPopup(text);}


function createDropdown(element,optionsArray,type,TextIdFunc,IdFunc,BehaviourFunc,htmlTag)
{//выпадающие списки
  let IsTextId = type=="text&id" ? true : false;
  let id = element.parentElement.firstElementChild.innerText;
  let new_td = document.createElement(htmlTag);
  let select = document.createElement('select');
  select.setAttribute('class', 'base');
  if (IsTextId)
  {optionsArray.forEach(([key, value]) => {
    const option = document.createElement('option');
    option.value = key; // Устанавливаем value для корректной работы Select2
    option.textContent = value; // Текст для отображения
    select.appendChild(option);
});} else
{optionsArray.forEach((value) => {
    const option = document.createElement('option');
    option.textContent = value; // Текст для отображения
    select.appendChild(option);
});
}
  select.selectedIndex = -1;
  let par_el = element.parentElement;
  new_td.setAttribute("name", element.getAttribute("Name"));
  element.replaceWith(new_td);
  new_td.appendChild(select);

  $(document).ready(function() {
        $('.base').select2({
            placeholder: "Выберите", // Место для подсказки
        });
        $('.base').on('select2:select', (e)=>{BehaviourFunc(e,element,new_td,id,type,IsTextId,TextIdFunc,IdFunc)});
    });
}

function MakeAddingRow(element){//При клике на +, добавление пустой новой строки и обработчиков событий
    if (Object.keys(new_row).length==0)
    {
        let tableBody = document.querySelector('table tbody');
        let newRow = document.createElement('tr');
        let columnCount = tableBody.rows[0] ? tableBody.rows[0].cells.length : 0;
        let headFields = document.querySelector('thead').children[0].children;
        sendData({"table_verbose_name_plural":model},element,element,"POST", "/addEmpty/")//Получение нового id
         .then(response =>
                {
                    new_id = response.id
                    for (let i = 0; i < columnCount; i++)
                        {
                            let newCell = document.createElement('td');
                            if (headFields[i].textContent != "")//чтобы нельзя было редактировать крестик для удаления
                            {newCell.ondblclick = function() { FillRow(this); };}
                            if (i==0) {newCell.textContent=new_id;new_row["id"]=new_id;} else
                            {
                                newCell.textContent = headFields[i].textContent != "" ? '-' : '';//пустая клетка для крестика для удаления
                                let tbody = tableBody.firstElementChild;
                                let name = tbody.children[i].getAttribute("Name");
                                newCell.setAttribute("name", name);
                                if (name=="third_name" || name=="category" || name=="diagnosis_id") {new_row[name]=null;};
                            };
                            newRow.appendChild(newCell);
                        }
                   tableBody.insertBefore(newRow, tableBody.firstChild);
                }
            )
            .catch(error => {
                console.error('Ошибка при добавлении строки:', error);
            });
    }
}

function FillRow(element){//редактируем поля которых нет в бд
    let list_fields = ["category","status","street","neighborhood_id","visit_id","diagnosis_id","doctor_id","patient_id","sex"];
    last_data = element.innerText;
    field = element.getAttribute("Name");
    if (list_fields.includes(field))//Если ячейка имеет тип данных - перечисление
    {
        element.focus();
        sendData({"field_name":field,"model_name":model},element,element,"POST", "/get_fields_by_name/")
        .then(response => {
        createDropdown(element,response.values,response.type,
        (type,selectedValue,id,element,selectedText,new_element)=>{ return sendData({"new_row":new_row,"type":type,"field_id":selectedValue,"id":id,"model_name":model,"field_name":element.getAttribute('name'),"last_data":element.innerText,"new_data":selectedText},element,new_element,"POST","/validate_field/")},
        (type,id,element,selectedText,new_element)=>{ return sendData({"new_row":new_row,"type":type,"id":id,"model_name":model,"field_name":element.getAttribute('name'),"last_data":element.innerText,"new_data":selectedText},element,new_element,"POST","/validate_field/")},
        ListForEdit,'td')})
        .catch(error => {
        console.error('Ошибка: ', error);
        });
        return
    }
    element.contentEditable = true;
    element.focus();
    enterIsPressed = false;
    element.onkeydown = (event) => {if (event.key === 'Enter' && !enterIsPressed)  {enterIsPressed=true; requestTextUpdate(event, element);}}
    element.onblur = (event) => {if (!enterIsPressed) {requestTextUpdate(event, element)} enterIsPressed = false;}
}
