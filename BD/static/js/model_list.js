
function getCsrfToken() {
  let match = document.cookie.split('csrftoken=')[1];
  if (match) return match;
  return null;
}
function makeEditable(element) {//при клике на ячейку она становится редактируемой
    if (user_group != "Пациенты")
    {
        const user_perm_arr_BD = user_perm.split(", ");
        const user_perm_arr = user_perm_arr_BD.map(item => item.split('.')[1]);
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
                sendData({"field_name":field,"model_name":model},element,"POST", "/get_fields_by_name/", true)
                .then(response => {
                createDropdown(element,response.values,response.type);//то создаётся выпадающий список
                })
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

function requestListUpdate (event,element,element_parent,text)
{
    children = element_parent.children;
    index = Array.prototype.indexOf.call(children, element);
    thead = document.querySelector('thead').firstElementChild;
    field_name = thead.children[index].innerText;
    let data = {
      "field":"list",
      "table_verbose_name_plural": model,
      "id": element.parentElement.firstElementChild.innerText,
      "field_name":field_name,
      "new_data":text,
    };
    sendData(data,element,"POST", "/change/",false);
}

function requestTextUpdate (event,element)
{
    element.contentEditable = false;
    children = element.parentElement.children;
    index = Array.prototype.indexOf.call(children, element);
    thead = document.querySelector('thead').firstElementChild;
    field_name = thead.children[index].innerText;
    let data = {
      "field":"text",
      "last_data":last_data,
      "table_verbose_name_plural": model,
      "id": element.parentElement.firstElementChild.innerText,
      "field_name":field_name,
      "new_data":element.innerText,
    };
    sendData(data,element,"POST", "/change/",false);
}

function sendData(data, element, method, dir, isReturn) {
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
                    element.classList.add('highlight-error');
                    element.innerText = last_data;
                    setTimeout(() => { element.classList.remove('highlight-error'); }, 1000);
                    reject(response); // Отклоняем промис с ошибкой
                }
            }
        };
        xhr.send(jsonData);
    });
}

function showPopup(text) {
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


function createDropdown(element,optionsArray,type) {
  let IsTextId = type=="text&id" ? true : false;
  let id = element.parentElement.firstElementChild.innerText;
  let new_td = document.createElement('td');
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
    console.log(type);
    console.log(optionsArray);
  select.selectedIndex = -1;
  let par_el = element.parentElement;
  element.replaceWith(new_td);
  new_td.appendChild(select);
  $(document).ready(function() {
        $('.base').select2({
            placeholder: "Выберите", // Место для подсказки
        });
        $('.base').on('select2:select', function(e) {
            let selectedText = e.params.data.text;
            if (IsTextId)
            {
                let selectedValue = e.params.data.id;
                sendData({"type":type,"field_id":selectedValue,"id":id,"model_name":model,"field_name":element.getAttribute('name'),"last_data":element.innerText,"new_data":selectedText},element,"POST","/change_by_list/",false)
            } else
            {
                sendData({"type":type,"id":id,"model_name":model,"field_name":element.getAttribute('name'),"last_data":element.innerText,"new_data":selectedText},element,"POST","/change_by_list/",false)

            }

        });
    });
}

function MakeAddingRow(element){//При клике на +, добавление пустой новой строки и обработчиков событий
    if (Object.keys(new_row).length==0)
    {
        let tableBody = document.querySelector('table tbody');
        let newRow = document.createElement('tr');
        let columnCount = tableBody.rows[0] ? tableBody.rows[0].cells.length : 0;
        sendData({"table_verbose_name_plural":model},element,"POST", "/addEmpty/", true)//Получение нового id
         .then(response =>
                {
                    new_id = response.id
                    for (let i = 0; i < columnCount; i++)
                        {
                            let newCell = document.createElement('td');
                            newCell.ondblclick = function() { FillRow(this); };
                            if (i==0) {newCell.textContent=new_id;new_row["id"]=new_id;} else
                            {
                                newCell.textContent = '-';
                                let tbody = tableBody.firstElementChild;
                                newCell.setAttribute("name", tbody.children[i].getAttribute("Name"));
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
    let list_fields = ["category","status","street","neighborhood_id","visit_id","diagnosis_id","doctor_id","patient_id"];
    last_data = element.innerText;
    field = element.getAttribute("Name");
    if (list_fields.includes(field))//Если ячейка имеет тип данных - перечисление
    {
        element.focus();
        sendData({"field_name":field,"model_name":model},element,"POST", "/get_fields_by_name/", true)
        .then(response => {
        createDropdown(element,response.values,response.type);//то создаётся выпадающий список
        })
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

function requestUpdateText (event,element,element_parent,text)
{
    children = element_parent.children;
    index = Array.prototype.indexOf.call(children, element);
    thead = document.querySelector('thead').firstElementChild;
    field_name = thead.children[index].innerText;
    let data = {
      "field":"list",
      "table_verbose_name_plural": model,
      "id": element.parentElement.firstElementChild.innerText,
      "field_name":field_name,
      "new_data":text,
    };
    sendData(data,element,"POST", "/change/",true)
    .then(response => {
            new_id = response.id
            for (let i = 0; i < columnCount; i++) {
                let newCell = document.createElement('td');
                newCell.ondblclick = function() { FillRow(this); };
                if (i==0) {newCell.textContent=new_id} else newCell.textContent = '-';
                newRow.appendChild(newCell);
            }
            tableBody.insertBefore(newRow, tableBody.firstChild);
        })
}