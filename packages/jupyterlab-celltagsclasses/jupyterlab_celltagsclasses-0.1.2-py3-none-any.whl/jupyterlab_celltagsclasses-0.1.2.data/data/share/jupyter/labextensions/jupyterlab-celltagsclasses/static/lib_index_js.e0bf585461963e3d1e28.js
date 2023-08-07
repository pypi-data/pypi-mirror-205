"use strict";
(self["webpackChunkjupyterlab_celltagsclasses"] = self["webpackChunkjupyterlab_celltagsclasses"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/*
 * for attaching keybindings later on, see
 * https://towardsdatascience.com/how-to-customize-jupyterlab-keyboard-shortcuts-72321f73753d
 */

/**
 * Initialization data for the jupyterlab-celltagsclasses extension.
 */
const plugin = {
    id: 'jupyterlab-celltagsclasses:plugin',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    activate: (app, notebookTracker) => {
        console.log('extension jupyterlab-celltagsclasses is activating');
        const class_for_tag = (tag) => `cell-tag-${tag}`;
        notebookTracker.widgetAdded.connect((_, panel) => {
            const notebookModel = panel.content.model;
            if (notebookModel === null) {
                return;
            }
            notebookModel.cells.changed.connect((cellList, change) => {
                if (change.type !== 'add') {
                    return;
                }
                change.newValues.forEach(cellModel => {
                    var _a, _b;
                    // compute widgets attached to cellModel
                    const cellWidgets = (_a = notebookTracker.currentWidget) === null || _a === void 0 ? void 0 : _a.content.widgets.filter((cell, index) => cell.model.id === cellModel.id);
                    if (cellWidgets === undefined || (cellWidgets === null || cellWidgets === void 0 ? void 0 : cellWidgets.length) === 0) {
                        console.warn('could not find cell widget for cell model', cellModel);
                        return;
                    }
                    console.debug(`found ${cellWidgets === null || cellWidgets === void 0 ? void 0 : cellWidgets.length} cell widgets`, cellWidgets[0]);
                    // add classes for pre-existing tags
                    (_b = cellModel.getMetadata('tags')) === null || _b === void 0 ? void 0 : _b.forEach((tag) => cellWidgets === null || cellWidgets === void 0 ? void 0 : cellWidgets.forEach(cellWidget => {
                        console.debug(`adding initial class for tag ${class_for_tag(tag)}`);
                        cellWidget.addClass(class_for_tag(tag));
                    }));
                    // react to changes in tags
                    cellModel.metadataChanged.connect((sender, change) => {
                        console.debug('metadata changed', sender, change);
                        if (change.key !== 'tags') {
                            // console.debug("ignoring non-tags metadata change")
                            return;
                        }
                        // does not seem useful to recompute this
                        // const cellWidgets = notebookTracker.currentWidget?.content.widgets.filter(
                        //   (cell: Cell, index: number) => (cell.model.id === cellModel.id)
                        // )
                        if (change.type === 'change') {
                            console.debug('change', change, change.newValue);
                            // compute difference between old and new tags
                            const oldTags = change.oldValue;
                            const newTags = change.newValue;
                            const addedTags = newTags.filter(tag => !oldTags.includes(tag));
                            const removedTags = oldTags.filter(tag => !newTags.includes(tag));
                            console.log('addedTags', addedTags);
                            console.log('removedTags', removedTags);
                            cellWidgets.forEach(cellWidget => {
                                addedTags.forEach(tag => {
                                    console.debug(`adding class for tag ${class_for_tag(tag)}`);
                                    cellWidget.addClass(class_for_tag(tag));
                                });
                                removedTags.forEach(tag => {
                                    console.debug(`removing class for tag ${class_for_tag(tag)}`);
                                    cellWidget.removeClass(class_for_tag(tag));
                                });
                            });
                        }
                        else if (change.type === 'add') {
                            console.log('add', change, change.newValue);
                            cellWidgets.forEach(cellWidget => {
                                for (const tag of change.newValue) {
                                    console.debug(`adding class for tag ${class_for_tag(tag)}`);
                                    cellWidget.addClass(class_for_tag(tag));
                                }
                            });
                        }
                        else if (change.type === 'remove') {
                            console.log('remove', change, change.newValue);
                            cellWidgets.forEach(cellWidget => {
                                for (const tag of change.newValue) {
                                    console.debug(`removing class for tag ${class_for_tag(tag)}`);
                                    cellWidget.removeClass(class_for_tag(tag));
                                }
                            });
                        }
                    });
                });
            });
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.e0bf585461963e3d1e28.js.map