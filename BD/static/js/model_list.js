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
                dict_fields ={"sex":["Мужчина","Женщина"],"category":["Первая","Вторая","Высшая"],"status":["Первичный","Вторичный"]};
                arr_fields = dict_fields[field];
                createDropdown(element,arr_fields);
                return
            }
            element.contentEditable = true;
            element.focus();
            enterIsPressed = false;//нужно т.к при вызове onkeydown вызывается сразу же onblur
            element.onkeydown = (event) => {if (event.key === 'Enter' && !enterIsPressed)  {enterIsPressed=true; handleEvent(event, element);}}
            element.onblur = (event) => {if (!enterIsPressed) {handleEvent(event, element)} enterIsPressed = false;}
        }
    }
}

function handleEvent(event,element)
{
    element.contentEditable = false;
    csrfToken = getCsrfToken();
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/change/", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.setRequestHeader("X-CSRFToken", csrfToken);
    parentElement = element.parentElement;
    children = parentElement.children;
    index = Array.prototype.indexOf.call(children, element);
    thead = document.querySelector('thead').children[0];
    field_name = thead.children[index].innerText;
    let data = {
      "last_data":last_data,
      "table_verbose_name_plural": model,
      "id": element.parentElement.firstElementChild.innerText,
      "field_name":field_name,
      "new_data":element.innerText,
    };
    let jsonData = JSON.stringify(data);
    xhr.onload = function ()
    {
      if (xhr.status == 200) {
      if (xhr.responseText!="")
            {let response = {};
            response = JSON.parse(xhr.responseText);}
            console.log("error");
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
  console.log(optionsArray);
  new_td = document.createElement('td');
  div_select_wrap = document.createElement('div');
  div_select_wrap.setAttribute('class', 'select-wrapper');
  div_select_arrow = document.createElement('div');
  div_select_arrow.setAttribute('class', 'select-arrow-3');
  select = document.createElement('select');
  option_result = optionsArray.map((value) => {
        return {
            value: String(value),
            text: String(value),
            selected: false
        };
    });
  console.log(option_result);
  option_result.forEach(optionText => {
    const option = document.createElement('option');
    option.value = option_result.value;
    option.textContent = optionText.text;
    select.appendChild(option);
  });
  element.replaceWith(new_td);
  new_td.appendChild(div_select_wrap);
  div_select_wrap.appendChild(select);
}

function createLanguageSelect(element,option_list) {
    select = document.createElement('select');
    select.setAttribute('size', option_list.length);
    option_result = option_list.map((value) => {
        return {
            value: value,
            text: value,
            selected: false
        };
    });
    option_result.forEach(language => {
        const option = document.createElement('option');
        option.value = option_result.value;
        option.textContent = language.text;
        if (language.selected) {
            option.selected = true;
        }
        select.appendChild(option);
    });
    element.replaceWith(select);
}