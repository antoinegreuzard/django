/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./app/static/app/js/bookForm.js":
/*!***************************************!*\
  !*** ./app/static/app/js/bookForm.js ***!
  \***************************************/
/***/ (() => {

eval("function getCookie(name) {\n  var cookieValue = null;\n  if (document.cookie && document.cookie !== '') {\n    var cookies = document.cookie.split(';');\n    for (var i = 0; i < cookies.length; i += 1) {\n      var cookie = cookies[i].trim();\n      if (cookie.substring(0, name.length + 1) === \"\".concat(name, \"=\")) {\n        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));\n        break;\n      }\n    }\n  }\n  return cookieValue;\n}\ndocument.addEventListener('DOMContentLoaded', function () {\n  document.getElementById('add-category-form').addEventListener('submit', function (e) {\n    e.preventDefault();\n    var categoryName = document.getElementById('category-name').value;\n    var data = {\n      categoryName: categoryName\n    };\n    fetch('/api/category/', {\n      body: JSON.stringify(data),\n      headers: {\n        'Content-Type': 'application/json',\n        'X-CSRFToken': getCookie('csrftoken')\n      },\n      method: 'POST'\n    }).then(function (response) {\n      return response.json();\n    }).then(function (responseData) {\n      if (responseData.success) {\n        alert('Catégorie ajoutée avec succès.');\n        window.location.reload();\n      } else {\n        alert(responseData.message || 'Une erreur est survenue.');\n      }\n    })[\"catch\"](function (error) {\n      console.error('Error:', error);\n    });\n  });\n});\n\n//# sourceURL=webpack://library/./app/static/app/js/bookForm.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./app/static/app/js/bookForm.js"]();
/******/ 	
/******/ })()
;