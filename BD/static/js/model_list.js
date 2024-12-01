function getCsrfToken() {
  let match = document.cookie.split('csrftoken=')[1];
  if (match) return match;
  return null;
}
function makeEditable(element) {
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
            let list_fields = ["sex","category","status"];
            last_data = element.innerText;
            field = element.getAttribute("Name");
            if (list_fields.includes(field))
            {
                element.focus();
                dict_fields ={"sex":["Мужчина","Женщина"],"category":["Первая","Вторая","Высшая"],"status":["Первичный","Вторичный"]};
                arr_fields = dict_fields[field];
                createDropdown(element,arr_fields);
                return
            }
            element.contentEditable = true;
            element.focus();
            enterIsPressed = false;//нужно т.к при вызове onkeydown вызывается сразу же onblur
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
    sendData(data,element);
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
    console.log(data)
    sendData(data,element);
}

function sendData(data,element) {
    csrfToken = getCsrfToken();
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/change/", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    let jsonData = JSON.stringify(data);
    xhr.onload = function ()
    {
      if (xhr.status == 200) {
      if (xhr.responseText!="")
            {let response = {};
            response = JSON.parse(xhr.responseText);}
      } else  {
        if (xhr.status!=304)
        {
            response = JSON.parse(xhr.responseText);
            showPopups(response.response);
            element.classList.add('highlight-error');
            element.innerText = last_data;
            setTimeout(() => {element.classList.remove('highlight-error');}, 1000);
        }
      }
    };
    xhr.send(jsonData);
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


function createDropdown(element,optionsArray) {
  new_td = document.createElement('td');
  div_select_wrap = document.createElement('div');
  div_select_wrap.setAttribute('class', 'select-wrapper');
  div_select_arrow = document.createElement('div');
  div_select_arrow.setAttribute('class', 'select-arrow-3');
  select = document.createElement('select');
  option_result = optionsArray.map((value) => {
        return {
            text: String(value),
            selected: false
        };
    });
  option_result.forEach(optionText => {
    const option = document.createElement('option');
    option.textContent = optionText.text;
    select.appendChild(option);
  });
  select.selectedIndex = -1;
  par_el = element.parentElement;
  element.replaceWith(new_td);
  new_td.appendChild(div_select_wrap);
  div_select_wrap.appendChild(select);
  select.addEventListener('change', function(event) {
    options_arr = event.target.getElementsByTagName('option')
    for (let cur_option of options_arr)
    {
        if (cur_option.selected)
            {
            requestListUpdate(event,new_td,par_el,cur_option.text)
            break;
            }
    }
});
}
