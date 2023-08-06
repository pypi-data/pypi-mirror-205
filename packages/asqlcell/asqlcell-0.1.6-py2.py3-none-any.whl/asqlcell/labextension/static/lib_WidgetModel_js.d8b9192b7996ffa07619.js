(self["webpackChunkasqlcell"] = self["webpackChunkasqlcell"] || []).push([["lib_WidgetModel_js"],{

/***/ "./lib/WidgetModel.js":
/*!****************************!*\
  !*** ./lib/WidgetModel.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.SqlCellView = exports.SqlCellModel = void 0;
const widgets = __importStar(__webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base"));
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_dom_1 = __importDefault(__webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom"));
const WidgetView_1 = __importDefault(__webpack_require__(/*! ./WidgetView */ "./lib/WidgetView.js"));
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const defaultModelProperties = {
    data_name: "",
    dfs_button: "",
    error: "",
    exec_time: "",
    output_var: "sqlcelldf",
    row_range: [0, 10],
    column_sort: ["", 0],
    dfs_result: "",
    sql_button: "",
    mode: "",
    data_grid: "",
    data_sql: "",
    vis_sql: ["", ""],
    vis_data: undefined,
    title_hist: "",
};
class SqlCellModel extends widgets.DOMWidgetModel {
    constructor() {
        super(...arguments);
        this.defaults = () => {
            return Object.assign(Object.assign({}, super.defaults()), { _model_name: SqlCellModel.model_name, _model_module: SqlCellModel.model_module, _model_module_version: SqlCellModel.model_module_version, _view_name: SqlCellModel.view_name, _view_module: SqlCellModel.view_module, _view_module_version: SqlCellModel.view_module_version, output_var: "sqlcelldf", row_range: undefined, column_sort: undefined, dfs_button: undefined, dfs_result: undefined, sql_button: undefined, mode: undefined, exec_time: "", data_grid: undefined, data_name: undefined, data_sql: undefined, error: undefined, vis_sql: undefined, vis_data: undefined, title_hist: undefined });
        };
    }
    initialize(attributes, options) {
        super.initialize(attributes, options);
        this.set("json_dump", new Date().toISOString());
        this.save_changes();
        // this.on("all", (msg) => { console.log(msg) })
        // this.on("change", (msg) => { console.log(msg) })
        this.on("change:output", this.handle_update_messages, this);
    }
    handle_update_messages(msg) {
        this.trigger("update_outputName", msg);
    }
}
exports.SqlCellModel = SqlCellModel;
SqlCellModel.serializers = Object.assign({}, widgets.DOMWidgetModel.serializers);
SqlCellModel.model_name = "SqlCellModel";
SqlCellModel.model_module = version_1.MODULE_NAME;
SqlCellModel.model_module_version = version_1.MODULE_VERSION;
SqlCellModel.view_name = "SqlCellView"; // Set to null if no view
SqlCellModel.view_module = version_1.MODULE_NAME; // Set to null if no view
SqlCellModel.view_module_version = version_1.MODULE_VERSION;
class SqlCellView extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.render = () => {
            this.el.classList.add("custom-widget");
            const component = react_1.default.createElement(WidgetView_1.default, {
                model: this.model,
            });
            react_dom_1.default.render(component, this.el);
        };
    }
}
exports.SqlCellView = SqlCellView;
//# sourceMappingURL=WidgetModel.js.map

/***/ }),

/***/ "./lib/WidgetView.js":
/*!***************************!*\
  !*** ./lib/WidgetView.js ***!
  \***************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const hooks_1 = __webpack_require__(/*! ./hooks */ "./lib/hooks.js");
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const table_1 = __webpack_require__(/*! ./table */ "./lib/table/index.js");
const input_1 = __webpack_require__(/*! ./input */ "./lib/input/index.js");
const visualization_1 = __webpack_require__(/*! ./visualization/visualization */ "./lib/visualization/visualization.js");
const line_1 = __webpack_require__(/*! ./visualization/line */ "./lib/visualization/line.js");
const ReactWidget = (props) => {
    var _a, _b, _c, _d, _e, _f, _g, _h, _j;
    const show = props.model.get("mode");
    const [data, setData] = react_1.useState(props.model.get("data_grid"));
    const [error, setError] = react_1.useState(props.model.get("error"));
    const [rowNumber, setRowNumber] = react_1.useState(props.model.get("row_range")[1] - props.model.get("row_range")[0]);
    const [page, setPage] = react_1.useState(Math.floor(props.model.get("row_range")[0] / rowNumber) + 1);
    const [tableState, setTableState] = react_1.useState(true);
    // Receive event from Model
    (_a = props.model) === null || _a === void 0 ? void 0 : _a.on("change:error", () => {
        setError(props.model.get("error"));
        setData("");
    });
    (_b = props.model) === null || _b === void 0 ? void 0 : _b.on("change:data_grid", () => {
        setData(props.model.get("data_grid"));
        setError("");
    });
    (_c = props.model) === null || _c === void 0 ? void 0 : _c.on("sort", (msg) => {
        var _a, _b;
        (_a = props.model) === null || _a === void 0 ? void 0 : _a.set("column_sort", msg, "");
        (_b = props.model) === null || _b === void 0 ? void 0 : _b.save_changes();
    });
    (_d = props.model) === null || _d === void 0 ? void 0 : _d.on("setRange", (msg) => {
        var _a, _b;
        (_a = props.model) === null || _a === void 0 ? void 0 : _a.set("row_range", msg, "");
        (_b = props.model) === null || _b === void 0 ? void 0 : _b.save_changes();
    });
    (_e = props.model) === null || _e === void 0 ? void 0 : _e.on("setTableView", (msg) => {
        setTableState(msg === 1 ? true : false);
    });
    (_f = props.model) === null || _f === void 0 ? void 0 : _f.on("vis_sql", (col_name) => {
        var _a, _b;
        (_a = props.model) === null || _a === void 0 ? void 0 : _a.set("vis_sql", [
            `select * EXCLUDE (index_rn1qaz2wsx)\nfrom \n(\nSELECT "${col_name}", ROW_NUMBER() OVER () AS index_rn1qaz2wsx\nFROM $$__NAME__$$\n)\nusing SAMPLE reservoir (100 rows) REPEATABLE(42)\norder by index_rn1qaz2wsx`,
            new Date().toISOString()
        ]);
        (_b = props.model) === null || _b === void 0 ? void 0 : _b.save_changes();
    });
    (_g = props.model) === null || _g === void 0 ? void 0 : _g.on("output_var", (outputName) => {
        var _a, _b;
        (_a = props.model) === null || _a === void 0 ? void 0 : _a.set("output_var", outputName);
        (_b = props.model) === null || _b === void 0 ? void 0 : _b.save_changes();
    });
    (_h = props.model) === null || _h === void 0 ? void 0 : _h.on("dfs_button", () => {
        var _a, _b;
        (_a = props.model) === null || _a === void 0 ? void 0 : _a.set("dfs_button", new Date().toISOString());
        (_b = props.model) === null || _b === void 0 ? void 0 : _b.save_changes();
    });
    (_j = props.model) === null || _j === void 0 ? void 0 : _j.on("data_sql", (sqlContent) => {
        var _a, _b;
        (_a = props.model) === null || _a === void 0 ? void 0 : _a.set("data_sql", sqlContent);
        (_b = props.model) === null || _b === void 0 ? void 0 : _b.save_changes();
    });
    return (react_1.default.createElement("div", { className: "Widget" },
        react_1.default.createElement(core_1.Stack, { spacing: 0, align: "center" },
            show === "UI" ?
                react_1.default.createElement(input_1.WidgetInputArea, { setPage: setPage })
                :
                    react_1.default.createElement(react_1.default.Fragment, null),
            error !== "" && data === "" ?
                react_1.default.createElement(core_1.Group, { position: "left" },
                    react_1.default.createElement(core_1.Text, { color: "red" }, "Error:"),
                    react_1.default.createElement(core_1.Text, null, error))
                :
                    react_1.default.createElement(react_1.default.Fragment, null),
            data !== "" ?
                react_1.default.createElement(core_1.Group, { sx: { width: "95%" }, position: "center" }, tableState ?
                    react_1.default.createElement(core_1.Tabs, { defaultValue: "table", sx: { width: "100%" } },
                        react_1.default.createElement(core_1.Tabs.List, null,
                            react_1.default.createElement(core_1.Tabs.Tab, { value: "table" }, "Table Result"),
                            react_1.default.createElement(core_1.Tabs.Tab, { value: "visualization" }, "Visualization")),
                        react_1.default.createElement(core_1.Tabs.Panel, { value: "table" },
                            react_1.default.createElement(table_1.DataTable, { page: page, setPage: setPage, rowNumber: rowNumber, setRowNumber: setRowNumber })),
                        react_1.default.createElement(core_1.Tabs.Panel, { value: "visualization" },
                            react_1.default.createElement(visualization_1.Visualization, null)))
                    :
                        react_1.default.createElement(line_1.LineChart, null))
                :
                    react_1.default.createElement(core_1.Box, { sx: { height: "60px" } }))));
};
const withModelContext = (Component) => {
    return (props) => (react_1.default.createElement(hooks_1.WidgetModelContext.Provider, { value: props.model },
        react_1.default.createElement(Component, Object.assign({}, props))));
};
exports["default"] = withModelContext(ReactWidget);
//# sourceMappingURL=WidgetView.js.map

/***/ }),

/***/ "./lib/hooks.js":
/*!**********************!*\
  !*** ./lib/hooks.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.useModel = exports.useModelEvent = exports.useModelState = exports.WidgetModelContext = void 0;
const react_1 = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
exports.WidgetModelContext = react_1.createContext(undefined);
// HOOKS
//============================================================================================
/**
 *
 * @param name property name in the Python model object.
 * @returns model state and set state function.
 */
function useModelState(name) {
    const model = useModel();
    const [state, setState] = react_1.useState(model === null || model === void 0 ? void 0 : model.get(name));
    useModelEvent(`change:${name}`, (model) => {
        setState(model.get(name));
    }, [name]);
    function updateModel(val, options) {
        model === null || model === void 0 ? void 0 : model.set(name, val, options);
        model === null || model === void 0 ? void 0 : model.save_changes();
    }
    return [state, updateModel];
}
exports.useModelState = useModelState;
/**
 * Subscribes a listener to the model event loop.
 * @param event String identifier of the event that will trigger the callback.
 * @param callback Action to perform when event happens.
 * @param deps Dependencies that should be kept up to date within the callback.
 */
function useModelEvent(event, callback, deps) {
    const model = useModel();
    const dependencies = deps === undefined ? [model] : [...deps, model];
    react_1.useEffect(() => {
        const callbackWrapper = (e) => model && callback(model, e);
        model === null || model === void 0 ? void 0 : model.on(event, callbackWrapper);
        return () => void (model === null || model === void 0 ? void 0 : model.unbind(event, callbackWrapper));
    }, dependencies);
}
exports.useModelEvent = useModelEvent;
/**
 * An escape hatch in case you want full access to the model.
 * @returns Python model
 */
function useModel() {
    return react_1.useContext(exports.WidgetModelContext);
}
exports.useModel = useModel;
//# sourceMappingURL=hooks.js.map

/***/ }),

/***/ "./lib/input/dataimport.js":
/*!*********************************!*\
  !*** ./lib/input/dataimport.js ***!
  \*********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.DataImport = void 0;
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const ri_1 = __webpack_require__(/*! react-icons/ri */ "./node_modules/react-icons/ri/index.esm.js");
const hooks_1 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const DataImport = () => {
    const model = hooks_1.useModel();
    const [opened, setOpened] = react_1.useState(false);
    const [dataframe, setDataFrame] = react_1.useState(model === null || model === void 0 ? void 0 : model.get("dfs_result"));
    model === null || model === void 0 ? void 0 : model.on("change:dfs_result", (msg) => {
        setDataFrame(model.get("dfs_result"));
    });
    const DropdownHeight = dataframe.trim().split(/\r?\n/).length >= 5 ? "125px" : `${dataframe.trim().split(/\r?\n/).length * 25}px`;
    const items = dataframe.split("\n").map((name, index) => (name === "" ?
        react_1.default.createElement(react_1.default.Fragment, null)
        :
            react_1.default.createElement(core_1.NavLink, { sx: { height: "25px" }, className: "data list", key: index, label: name.split("\t")[0], onClick: () => {
                    model === null || model === void 0 ? void 0 : model.trigger("importData", name.split("\t")[0]);
                    setOpened(false);
                }, rightSection: react_1.default.createElement(core_1.Text, { size: "xs" }, name.split("\t")[1]) })));
    return (react_1.default.createElement(react_1.default.Fragment, null,
        react_1.default.createElement(core_1.Popover, { opened: opened, onChange: setOpened },
            react_1.default.createElement(core_1.Popover.Target, null,
                react_1.default.createElement(core_1.Button, { rightIcon: react_1.default.createElement(ri_1.RiArrowDownSLine, null), color: "dark", variant: "subtle", radius: "xs", sx: {
                        outline: "none",
                        "&:hover": {
                            backgroundColor: "transparent"
                        },
                    }, onClick: () => {
                        setOpened((open) => !open);
                        model === null || model === void 0 ? void 0 : model.trigger("dfs_button");
                    } },
                    react_1.default.createElement(core_1.Text, { color: "gray", sx: { fontWeight: "bold" } }, "Dataframe"))),
            react_1.default.createElement(core_1.Popover.Dropdown, { sx: {
                    marginLeft: "2.5%",
                    marginTop: "-15px",
                    padding: "2px",
                } }, dataframe ?
                react_1.default.createElement(core_1.ScrollArea, { sx: { height: DropdownHeight } },
                    react_1.default.createElement(core_1.Group, { style: { width: "100%" } },
                        react_1.default.createElement(core_1.Box, { sx: {
                                padding: 0,
                            } }, items)))
                :
                    react_1.default.createElement(core_1.Text, { color: "lightgray" }, "There is no dataframe.")))));
};
exports.DataImport = DataImport;
//# sourceMappingURL=dataimport.js.map

/***/ }),

/***/ "./lib/input/index.js":
/*!****************************!*\
  !*** ./lib/input/index.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
__exportStar(__webpack_require__(/*! ./dataimport */ "./lib/input/dataimport.js"), exports);
__exportStar(__webpack_require__(/*! ./outputname */ "./lib/input/outputname.js"), exports);
__exportStar(__webpack_require__(/*! ./inputarea */ "./lib/input/inputarea.js"), exports);
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "./lib/input/inputarea.js":
/*!********************************!*\
  !*** ./lib/input/inputarea.js ***!
  \********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.WidgetInputArea = void 0;
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const react_1 = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
const dataimport_1 = __webpack_require__(/*! ./dataimport */ "./lib/input/dataimport.js");
const outputname_1 = __webpack_require__(/*! ./outputname */ "./lib/input/outputname.js");
const vsc_1 = __webpack_require__(/*! react-icons/vsc */ "./node_modules/react-icons/vsc/index.esm.js");
const react_2 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const hooks_1 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const WidgetInputArea = ({ setPage }) => {
    const model = hooks_1.useModel();
    const [sqlContent, setSqlContent] = react_1.useState(model === null || model === void 0 ? void 0 : model.get("data_sql"));
    model === null || model === void 0 ? void 0 : model.on("importData", (msg) => {
        setSqlContent("select * from " + msg);
    });
    react_1.useEffect(() => {
        model === null || model === void 0 ? void 0 : model.trigger("data_sql", sqlContent);
    }, [sqlContent]);
    return (react_2.default.createElement(react_2.default.Fragment, null,
        react_2.default.createElement(core_1.Group, { position: "apart", align: "center", sx: {
                width: "95%",
                height: "30px",
            } },
            react_2.default.createElement(dataimport_1.DataImport, null),
            react_2.default.createElement(outputname_1.NameOutput, null)),
        react_2.default.createElement(core_1.Group, { sx: {
                width: "95%",
                display: "flex",
                gap: 0,
            } },
            react_2.default.createElement(core_1.Box, { sx: {
                    width: "95%"
                } },
                react_2.default.createElement(core_1.Textarea, { autosize: true, minRows: 3, sx: {
                        marginTop: "10px",
                        ".mantine-Textarea-input": {
                            height: "88px",
                        }
                    }, value: sqlContent, onChange: (e) => {
                        setSqlContent(e.target.value);
                    } })),
            react_2.default.createElement(core_1.ActionIcon, { onClick: () => {
                    model === null || model === void 0 ? void 0 : model.set("sql_button", new Date().toISOString());
                    model === null || model === void 0 ? void 0 : model.set("data_sql", sqlContent);
                    model === null || model === void 0 ? void 0 : model.set("error", "");
                    model === null || model === void 0 ? void 0 : model.save_changes();
                    setPage(1);
                }, sx: { height: "100%" } },
                react_2.default.createElement(vsc_1.VscDebugStart, { size: 18 })))));
};
exports.WidgetInputArea = WidgetInputArea;
//# sourceMappingURL=inputarea.js.map

/***/ }),

/***/ "./lib/input/outputname.js":
/*!*********************************!*\
  !*** ./lib/input/outputname.js ***!
  \*********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.NameOutput = void 0;
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const hooks_1 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const NameOutput = () => {
    const model = hooks_1.useModel();
    const [outputName, setOutputName] = react_1.useState(model === null || model === void 0 ? void 0 : model.get("output_var"));
    model === null || model === void 0 ? void 0 : model.on("update_outputName", (msg) => {
        setOutputName(msg.changed.output);
    });
    const escape = () => {
        if (document.activeElement instanceof HTMLElement) {
            if (outputName.trim().length > 0) {
                model === null || model === void 0 ? void 0 : model.trigger("output_var", outputName);
                document.activeElement.blur();
            }
            else {
                setOutputName(model === null || model === void 0 ? void 0 : model.get("output_var"));
            }
        }
    };
    return (react_1.default.createElement(core_1.Group, { position: "right", align: "center", sx: {
            height: "100%",
            gap: "0px",
        } },
        react_1.default.createElement(core_1.Text, { color: "#8D8D8D", sx: { marginRight: "10px" } }, "SAVED TO"),
        react_1.default.createElement(core_1.TextInput, { size: "xs", styles: () => ({
                input: {
                    width: "100px",
                    color: "#8D8D8D",
                    fontSize: "inherit",
                    backgroundColor: "#fafafa",
                    borderColor: "#fafafa",
                    fontWeight: "bold",
                    paddingLeft: 0,
                    ":focus": {
                        borderColor: outputName.trim().length === 0 ? "red" : "lightgray",
                    }
                },
            }), value: outputName, onBlur: () => {
                escape();
            }, onKeyDown: (e) => {
                if (["Enter", "Escape"].includes(e.code)) {
                    e.preventDefault();
                    escape();
                }
            }, onChange: (e) => {
                setOutputName(e.target.value);
            } })));
};
exports.NameOutput = NameOutput;
//# sourceMappingURL=outputname.js.map

/***/ }),

/***/ "./lib/table/element.js":
/*!******************************!*\
  !*** ./lib/table/element.js ***!
  \******************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.TableElement = void 0;
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const vsc_1 = __webpack_require__(/*! react-icons/vsc */ "./node_modules/react-icons/vsc/index.esm.js");
const hooks_1 = __webpack_require__(/*! @mantine/hooks */ "webpack/sharing/consume/default/@mantine/hooks/@mantine/hooks?07de");
const TableElement = ({ item }) => {
    const { ref, width } = hooks_1.useElementSize();
    return (react_1.default.createElement(core_1.Popover, { position: "top", withArrow: true, shadow: "md" },
        react_1.default.createElement(core_1.Group, { ref: ref, noWrap: true, sx: { gap: 0 } },
            react_1.default.createElement(core_1.Text, { sx: { overflow: "hidden" }, fz: "8px" }, item),
            react_1.default.createElement(core_1.Popover.Target, null, width < (8 * item.length - 40) ?
                react_1.default.createElement(core_1.ActionIcon, { variant: "light", color: "blue", sx: { height: "10px", minHeight: "10px", width: "10px", minWidth: "10px" } },
                    react_1.default.createElement(vsc_1.VscEllipsis, { size: 8 }))
                :
                    react_1.default.createElement("div", null))),
        react_1.default.createElement(core_1.Popover.Dropdown, { sx: { padding: 0 } },
            react_1.default.createElement(core_1.Textarea, { readOnly: true, variant: "unstyled", withAsterisk: true, defaultValue: item, autosize: true, minRows: 1, maxRows: 2, sx: {
                    fontSize: "12px",
                    "& .mantine-Textarea-input": {
                        cursor: "default",
                        paddingTop: 0,
                        paddingBottom: 0,
                    }
                } }))));
};
exports.TableElement = TableElement;
//# sourceMappingURL=element.js.map

/***/ }),

/***/ "./lib/table/header.js":
/*!*****************************!*\
  !*** ./lib/table/header.js ***!
  \*****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.DataframeHeader = void 0;
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const icons_react_1 = __webpack_require__(/*! @tabler/icons-react */ "webpack/sharing/consume/default/@tabler/icons-react/@tabler/icons-react");
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const fa_1 = __webpack_require__(/*! react-icons/fa */ "./node_modules/react-icons/fa/index.esm.js");
const hooks_1 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const bar_1 = __webpack_require__(/*! ../visualization/bar */ "./lib/visualization/bar.js");
const line_1 = __webpack_require__(/*! ../visualization/line */ "./lib/visualization/line.js");
const HeaderInfo = ({ headerContent, item, dataLength }) => {
    const model = hooks_1.useModel();
    const [open, setOpen] = react_1.useState(undefined);
    return (react_1.default.createElement(react_1.default.Fragment, null, headerContent.filter(header => header.columnName === item && (header.dtype.includes("int") || header.dtype.includes("float"))).length !== 0 ?
        react_1.default.createElement(core_1.Group, { noWrap: true, position: "center", sx: { gap: 0, alignItems: "flex-start" } },
            react_1.default.createElement(bar_1.BarChart, { item: item, headerContent: headerContent }),
            react_1.default.createElement(core_1.Popover, { onOpen: () => {
                    model === null || model === void 0 ? void 0 : model.trigger("vis_sql", item);
                } },
                react_1.default.createElement(core_1.Popover.Target, null,
                    react_1.default.createElement(core_1.ActionIcon, { variant: "transparent", sx: { alignItems: "flex-end" } },
                        react_1.default.createElement(icons_react_1.IconChartLine, { size: 12 }))),
                react_1.default.createElement(core_1.Popover.Dropdown, { sx: {
                        position: "fixed",
                        top: "calc(50vh - 75px) !important",
                        left: "calc(50vw - 240px) !important",
                    } },
                    react_1.default.createElement(line_1.LineChart, null))))
        :
            react_1.default.createElement(core_1.Stack, { align: "left", sx: { gap: 0 } }, headerContent.filter(header => header.columnName === item).length > 0 ?
                headerContent.filter(header => header.columnName === item)[0].bins.map(bin => {
                    return (react_1.default.createElement(core_1.Group, { noWrap: true, position: "apart", onMouseEnter: () => { setOpen(item); }, onMouseLeave: () => setOpen(undefined), sx: { gap: 0, width: "10rem", marginBottom: "-2px" } }, bin.count !== 0 ?
                        react_1.default.createElement(react_1.default.Fragment, null,
                            react_1.default.createElement(core_1.Box, { sx: { maxWidth: "6rem" } },
                                react_1.default.createElement(core_1.Text, { weight: 600, fs: "italic", c: "#696969", truncate: true, fz: "xs" }, bin.bin)),
                            open ?
                                react_1.default.createElement(core_1.Text, { c: "blue", fz: "xs" }, bin.count)
                                :
                                    react_1.default.createElement(core_1.Text, { c: "blue", fz: "xs" },
                                        (bin.count / dataLength * 100).toFixed(2),
                                        "%"))
                        :
                            react_1.default.createElement(react_1.default.Fragment, null)));
                })
                :
                    react_1.default.createElement(react_1.default.Fragment, null))));
};
const HeaderTitle = ({ headerContent, item }) => {
    const model = hooks_1.useModel();
    const Order = {
        Increasing: 1,
        Descending: -1,
        None: 0,
    };
    const [order, setOrder] = react_1.useState(model === null || model === void 0 ? void 0 : model.get("column_sort")[1]);
    let currentOrder = Order.None;
    const [col, setColName] = react_1.useState(model === null || model === void 0 ? void 0 : model.get("column_sort")[0]);
    return (react_1.default.createElement(core_1.Group, { position: "center" },
        react_1.default.createElement(core_1.Button, { color: "dark", sx: {
                maxWidth: "10rem",
                height: "27px",
                "&.mantine-UnstyledButton-root": {
                    ":hover": {
                        backgroundColor: "#ebebeb",
                    }
                }
            }, rightIcon: react_1.default.createElement(react_1.default.Fragment, null,
                headerContent ?
                    headerContent.filter(header => header.columnName === item).length !== 0 ?
                        react_1.default.createElement(core_1.Text, { size: "xs", fs: "italic", color: "gray" }, headerContent.filter(header => header.columnName === item)[0].dtype.includes("datetime") ?
                            "datetime"
                            :
                                headerContent.filter(header => header.columnName === item)[0].dtype)
                        :
                            react_1.default.createElement(react_1.default.Fragment, null)
                    :
                        react_1.default.createElement(react_1.default.Fragment, null),
                col === item ?
                    order === Order.Increasing ?
                        react_1.default.createElement(fa_1.FaSortUp, { color: "gray", size: 10 })
                        :
                            order === Order.Descending ?
                                react_1.default.createElement(fa_1.FaSortDown, { color: "gray", size: 10 })
                                :
                                    react_1.default.createElement(fa_1.FaSort, { color: "lightgray", size: 10 })
                    :
                        react_1.default.createElement(fa_1.FaSort, { color: "lightgray", size: 10 })), variant: "subtle", onClick: () => {
                if (col === item) {
                    if (order === Order.Increasing) {
                        currentOrder = Order.Descending;
                        setOrder(Order.Descending);
                    }
                    else if (order === Order.Descending) {
                        currentOrder = Order.None;
                        setOrder(Order.None);
                    }
                    else {
                        currentOrder = Order.Increasing;
                        setOrder(Order.Increasing);
                    }
                }
                else {
                    currentOrder = Order.Increasing;
                    setOrder(Order.Increasing);
                    setColName(item);
                }
                model === null || model === void 0 ? void 0 : model.trigger("sort", [item, currentOrder]);
            } },
            react_1.default.createElement(core_1.Text, { truncate: true, fw: 700 }, item))));
};
const DataframeHeader = ({ headerContent, header, dataLength }) => {
    return (react_1.default.createElement("thead", null,
        react_1.default.createElement("tr", null,
            react_1.default.createElement("th", null),
            header.map((item, index) => react_1.default.createElement("th", { key: index, style: {
                    padding: 0,
                    verticalAlign: "baseline",
                } },
                react_1.default.createElement(core_1.Box, { sx: {
                        display: "flex",
                        justifyContent: "center",
                    } },
                    react_1.default.createElement(core_1.Stack, { align: "center", sx: { gap: 0, maxWidth: "10rem" } },
                        react_1.default.createElement(HeaderTitle, { headerContent: headerContent, item: item }),
                        headerContent ?
                            react_1.default.createElement(HeaderInfo, { headerContent: headerContent, item: item, dataLength: dataLength })
                            :
                                react_1.default.createElement(react_1.default.Fragment, null))))))));
};
exports.DataframeHeader = DataframeHeader;
//# sourceMappingURL=header.js.map

/***/ }),

/***/ "./lib/table/index.js":
/*!****************************!*\
  !*** ./lib/table/index.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
__exportStar(__webpack_require__(/*! ./header */ "./lib/table/header.js"), exports);
__exportStar(__webpack_require__(/*! ./table */ "./lib/table/table.js"), exports);
//# sourceMappingURL=index.js.map

/***/ }),

/***/ "./lib/table/table.js":
/*!****************************!*\
  !*** ./lib/table/table.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.DataTable = void 0;
const react_1 = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const react_2 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const header_1 = __webpack_require__(/*! ./header */ "./lib/table/header.js");
const element_1 = __webpack_require__(/*! ./element */ "./lib/table/element.js");
const hooks_1 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const DataTable = ({ page, setPage, rowNumber, setRowNumber }) => {
    var _a, _b, _c;
    const model = hooks_1.useModel();
    const [data, setData] = react_1.useState((_a = model === null || model === void 0 ? void 0 : model.get("data_grid")) !== null && _a !== void 0 ? _a : "{}");
    model === null || model === void 0 ? void 0 : model.on("change:data_grid", () => { setData(model.get("data_grid")); });
    const [hist, setHist] = react_1.useState((_b = model === null || model === void 0 ? void 0 : model.get("title_hist")) !== null && _b !== void 0 ? _b : "");
    model === null || model === void 0 ? void 0 : model.on("change:title_hist", () => setHist(model === null || model === void 0 ? void 0 : model.get("title_hist")));
    const [execTime, setExecTime] = react_1.useState((_c = model === null || model === void 0 ? void 0 : model.get("exec_time")) !== null && _c !== void 0 ? _c : "");
    model === null || model === void 0 ? void 0 : model.on("execTime", (msg) => setExecTime(msg.slice(9, msg.length)));
    const [tempoIndex, setTempoIndex] = react_1.useState(1);
    const [outOfRange, setOutOfRange] = react_1.useState(false);
    const info = JSON.parse(data.split("\n")[0]);
    const dataLength = data.split("\n")[1] || 0;
    const header = info.columns;
    let timeDiff = 0;
    if (execTime.length !== 0) {
        timeDiff = (new Date(execTime.split(",")[1]).getTime() - new Date(execTime.split(",")[0]).getTime()) / 1000;
    }
    const headerContent = hist ?
        JSON.parse(hist)
        :
            [{ columnName: "", dtype: "", bins: [{ bin_start: 0, bin_end: 0, count: 0 }] }];
    const rows = [...Array(info.index.length).keys()].map((index) => (react_2.default.createElement("tr", { key: base_1.uuid() },
        react_2.default.createElement("td", { key: index }, info.index[index]),
        info.data[index].map((item, tdIndex) => (react_2.default.createElement("td", { key: tdIndex, style: { fontSize: "8px" } }, typeof (item) === "boolean" ?
            item ?
                "True"
                :
                    "False"
            :
                typeof (item) === "string" && item.length > 30 ?
                    react_2.default.createElement(element_1.TableElement, { item: item })
                    :
                        item))))));
    return (react_2.default.createElement(core_1.Stack, { align: "center", spacing: 10, sx: {
            width: "100%",
            marginBottom: "16px",
        } },
        react_2.default.createElement(core_1.ScrollArea, { scrollbarSize: 8, style: { width: "100%" } },
            react_2.default.createElement(core_1.Table, { withBorder: true, withColumnBorders: true, striped: true, sx: {
                    width: "100%",
                    "& thead": {
                        height: "57px",
                    },
                    "& td": {
                        maxWidth: "200px"
                    },
                    "& tbody tr td": {
                        padding: "0px 3px",
                    },
                    "&  td:first-of-type": {
                        backgroundColor: "#ebebeb",
                        width: "7%"
                    },
                    "&  tr:first-of-type": {
                        backgroundColor: "#ebebeb",
                    },
                    "&  tr:nth-of-type(even)": {
                        backgroundColor: "#f2f2f2",
                    },
                } },
                react_2.default.createElement(header_1.DataframeHeader, { headerContent: headerContent, header: header, dataLength: dataLength }),
                react_2.default.createElement("tbody", null, rows))),
        react_2.default.createElement(core_1.Group, { position: "apart", sx: { width: "100%" } },
            react_2.default.createElement(core_1.Group, null,
                react_2.default.createElement(core_1.Text, { color: "#8d8d8d" },
                    dataLength,
                    " rows"),
                timeDiff !== 0 ?
                    react_2.default.createElement(core_1.Text, { color: "#8d8d8d" },
                        timeDiff,
                        " s")
                    :
                        react_2.default.createElement(react_2.default.Fragment, null)),
            react_2.default.createElement(core_1.Group, { align: "center" },
                react_2.default.createElement(core_1.Group, { sx: { gap: 0 } },
                    react_2.default.createElement(core_1.Select, { sx: {
                            width: "40px",
                            height: "22px",
                            ".mantine-Select-item": { padding: "0px" },
                            ".mantine-Select-rightSection": { width: "20px" },
                            ".mantine-Select-input": {
                                paddingLeft: "1px",
                                paddingRight: "0px",
                                height: "22px",
                                minHeight: "22px",
                                color: "#8d8d8d",
                            },
                        }, placeholder: rowNumber, data: ["10", "30", "50", "100"], onChange: (number) => {
                            const num = number;
                            setPage(1);
                            setRowNumber(num);
                            model === null || model === void 0 ? void 0 : model.trigger("setRange", [(0 * num), 1 * num]);
                        } }),
                    react_2.default.createElement(core_1.Text, { color: "#8d8d8d" }, "/page")),
                data ?
                    react_2.default.createElement(core_1.Pagination, { size: "xs", page: page, total: Math.ceil(dataLength / rowNumber), onChange: (index) => {
                            setPage(index);
                            model === null || model === void 0 ? void 0 : model.trigger("setRange", [((index - 1) * rowNumber), index * rowNumber]);
                        }, styles: (theme) => ({
                            item: {
                                color: theme.colors.gray[4],
                                backgroundColor: theme.colors.gray[0],
                                "&[data-active]": {
                                    color: theme.colors.dark[2],
                                    backgroundColor: theme.colors.gray[4],
                                },
                            },
                        }) })
                    :
                        react_2.default.createElement(react_2.default.Fragment, null),
                react_2.default.createElement(core_1.Group, { sx: { gap: 0 } },
                    react_2.default.createElement(core_1.Text, { color: "#8d8d8d" }, "goto"),
                    react_2.default.createElement(core_1.NumberInput, { defaultValue: 18, size: "xs", hideControls: true, error: outOfRange, value: page, onBlur: () => {
                            if (tempoIndex > 0 && tempoIndex <= Math.ceil(dataLength / rowNumber)) {
                                setPage(tempoIndex);
                                setOutOfRange(false);
                                model === null || model === void 0 ? void 0 : model.trigger("setRange", [((tempoIndex - 1) * rowNumber), tempoIndex * rowNumber]);
                            }
                            else {
                                setOutOfRange(true);
                            }
                        }, onKeyDown: (e) => {
                            if (["Escape", "Enter"].indexOf(e.key) > -1) {
                                (document.activeElement instanceof HTMLElement) && document.activeElement.blur();
                                if (tempoIndex > 0 && tempoIndex <= Math.ceil(dataLength / rowNumber)) {
                                    setPage(tempoIndex);
                                    setOutOfRange(false);
                                    model === null || model === void 0 ? void 0 : model.trigger("setRange", [((tempoIndex - 1) * rowNumber), tempoIndex * rowNumber]);
                                }
                                else {
                                    setOutOfRange(true);
                                }
                            }
                        }, onChange: (page) => {
                            setTempoIndex(page);
                            (page > 0 && page <= Math.ceil(dataLength / rowNumber)) ?
                                setOutOfRange(false)
                                :
                                    setOutOfRange(true);
                        }, sx: {
                            width: "40px",
                            ".mantine-NumberInput-input": {
                                paddingLeft: "5px",
                                paddingRight: "0px",
                                height: "22px",
                                minHeight: "22px",
                            }
                        } }))))));
};
exports.DataTable = DataTable;
//# sourceMappingURL=table.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/visualization/bar.js":
/*!**********************************!*\
  !*** ./lib/visualization/bar.js ***!
  \**********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.BarChart = void 0;
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_vega_1 = __webpack_require__(/*! react-vega */ "webpack/sharing/consume/default/react-vega/react-vega");
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const BarChart = ({ item, headerContent }) => {
    const expo = (input) => { return input.toExponential(2); };
    const isScientific = (input) => { return (!(0.1 <= Math.abs(input) && Math.abs(input) <= 10000)); };
    const getIntervalSide = (input) => {
        let res = "";
        if (input === 0) {
            res = "0";
        }
        else if (isScientific(input)) {
            res = expo(input);
        }
        else {
            res = input.toFixed(2);
        }
        return res;
    };
    const globalInterval = (item) => {
        const left = headerContent.filter(header => header.columnName === item)[0].bins[0].bin_start;
        const right = headerContent.filter(header => header.columnName === item)[0].bins[9].bin_end;
        return (`[${getIntervalSide(left)}, ${getIntervalSide(right)}]`);
    };
    const data = headerContent.filter(header => header.columnName === item)[0].bins;
    const barData = {
        table: data.map((item, index) => {
            const leftInterval = getIntervalSide(item.bin_start);
            const rightInterval = getIntervalSide(item.bin_end);
            const interval = `[${leftInterval}, ${rightInterval}]`;
            return ({ a: interval, b: item.count, index: index });
        }),
    };
    return (react_1.default.createElement(core_1.Stack, null,
        react_1.default.createElement(react_vega_1.VegaLite, { data: barData, actions: false, spec: {
                "background": "transparent",
                "data": { "name": "table" },
                "width": 60,
                "height": 40,
                "config": { "view": { "stroke": null } },
                "layer": [
                    {
                        "params": [
                            {
                                "name": "hover",
                                "select": { "type": "point", "on": "mouseover", "clear": "mouseout" }
                            }
                        ],
                        "mark": { "type": "bar", "color": "#eee", "tooltip": true },
                        "transform": [
                            {
                                "calculate": "datum.a + ': ' +datum.b", "as": "tooltip",
                            }
                        ],
                        "encoding": {
                            "x": {
                                "field": "index",
                                "type": "nominal",
                                "axis": { "labels": false, "title": null },
                            },
                            "tooltip": { "field": "tooltip", "type": "nominal" },
                            "opacity": {
                                "condition": { "test": { "param": "hover", "empty": false }, "value": 0.5 },
                                "value": 0
                            },
                            "detail": [{ "field": "count" }]
                        }
                    },
                    {
                        "mark": "bar",
                        "transform": [{
                                "calculate": "datum.b===0 ? 0 : datum.b === 1? 0.5: log(datum.b)/log(2)", "as": "log_x"
                            }],
                        "encoding": {
                            "x": {
                                "field": "index",
                                "type": "nominal",
                                "axis": { "labels": false, "title": null, "ticks": false },
                            },
                            "y": {
                                "field": "log_x",
                                "type": "quantitative",
                                "axis": { "labels": false, "domain": false, "grid": false, "ticks": false, "title": null },
                            },
                        }
                    },
                ]
            } }),
        react_1.default.createElement(core_1.Group, { sx: { width: "max-content" } },
            react_1.default.createElement(core_1.Text, { size: "xs", c: "#696969", sx: { marginTop: "-20px" } }, globalInterval(item)))));
};
exports.BarChart = BarChart;
//# sourceMappingURL=bar.js.map

/***/ }),

/***/ "./lib/visualization/line.js":
/*!***********************************!*\
  !*** ./lib/visualization/line.js ***!
  \***********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.LineChart = void 0;
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_vega_1 = __webpack_require__(/*! react-vega */ "webpack/sharing/consume/default/react-vega/react-vega");
const hooks_1 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const LineChart = () => {
    const model = hooks_1.useModel();
    const [data, setData] = react_1.useState((model === null || model === void 0 ? void 0 : model.get("vis_data")) !== "" ? model === null || model === void 0 ? void 0 : model.get("vis_data") : `{\"columns\":[],\"index\":[],\"data\":[]}`);
    const colData = JSON.parse(data).data;
    const colName = JSON.parse(data).columns[0];
    model === null || model === void 0 ? void 0 : model.on("change:vis_data", (msg) => {
        setData(model.get("vis_data"));
    });
    const lineData = colData ?
        {
            values: colData.map((item, index) => {
                return ({ a: index, b: item });
            })
        }
        :
            {
                values: [
                    { 'a': 0, 'b': 0 }
                ]
            };
    const dataLength = lineData.values.length;
    return react_1.default.createElement(react_vega_1.VegaLite, { data: lineData, actions: false, spec: {
            width: 400,
            height: 150,
            params: [{
                    name: "industry",
                    select: { type: "point", fields: ["series"] },
                    bind: "legend"
                }],
            layer: [
                {
                    mark: 'line',
                    transform: [
                        { calculate: "datum.a", as: "index" },
                        { calculate: "datum.b", as: colName }
                    ],
                    encoding: {
                        x: { field: "index", type: dataLength >= 10 ? "quantitative" : "ordinal", axis: { title: null } },
                        y: { field: colName, type: "quantitative" },
                        opacity: {
                            condition: { param: "industry", value: 1 },
                            value: 10
                        }
                    },
                    data: { name: 'values' }
                }
            ]
        } });
};
exports.LineChart = LineChart;
//# sourceMappingURL=line.js.map

/***/ }),

/***/ "./lib/visualization/visualization.js":
/*!********************************************!*\
  !*** ./lib/visualization/visualization.js ***!
  \********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.Visualization = void 0;
const core_1 = __webpack_require__(/*! @mantine/core */ "webpack/sharing/consume/default/@mantine/core/@mantine/core");
const hooks_1 = __webpack_require__(/*! @mantine/hooks */ "webpack/sharing/consume/default/@mantine/hooks/@mantine/hooks?07de");
const icons_react_1 = __webpack_require__(/*! @tabler/icons-react */ "webpack/sharing/consume/default/@tabler/icons-react/@tabler/icons-react");
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const react_vega_1 = __webpack_require__(/*! react-vega */ "webpack/sharing/consume/default/react-vega/react-vega");
const hooks_2 = __webpack_require__(/*! ../hooks */ "./lib/hooks.js");
const VisualMenu = ({ chartType, setChartType, setXAxis, setColName, colName, header }) => {
    const model = hooks_2.useModel();
    model === null || model === void 0 ? void 0 : model.on("change:vis_data", () => { var _a; setColName((_a = JSON.parse(model === null || model === void 0 ? void 0 : model.get("vis_data")).columns[0]) !== null && _a !== void 0 ? _a : ""); });
    return (react_1.default.createElement(core_1.Stack, { h: "100%", sx: { minWidth: "15rem" } },
        react_1.default.createElement(core_1.Tabs, { variant: "pills", defaultValue: "data" },
            react_1.default.createElement(core_1.Tabs.List, { grow: true },
                react_1.default.createElement(core_1.Group, { noWrap: true },
                    react_1.default.createElement(core_1.Tabs.Tab, { value: "data" }, "Data"))),
            react_1.default.createElement(core_1.Tabs.Panel, { value: "data" },
                react_1.default.createElement(core_1.Grid, { sx: { marginTop: "1rem" } },
                    react_1.default.createElement(core_1.Grid.Col, { span: 10 },
                        react_1.default.createElement(core_1.Select, { icon: chartType === 1 ? react_1.default.createElement(icons_react_1.IconChartLine, null) : react_1.default.createElement(icons_react_1.IconChartBar, null), label: "Chart Type", defaultValue: "1", data: [
                                { value: "1", label: "Line" },
                                { value: "2", label: "Bar" }
                            ], onChange: (value) => { setChartType(parseInt(value)); } })),
                    react_1.default.createElement(core_1.Grid.Col, { span: 2 }),
                    react_1.default.createElement(core_1.Grid.Col, { span: 10 },
                        react_1.default.createElement(core_1.Select, { label: "X-axis", defaultValue: "Index", data: ["Index"], onChange: (value) => { setXAxis(value); } })),
                    react_1.default.createElement(core_1.Grid.Col, { span: 2, sx: { display: "flex", alignItems: "end" } }),
                    react_1.default.createElement(core_1.Grid.Col, { span: 10 },
                        react_1.default.createElement(core_1.Select, { label: "Y-axis 1", value: colName, data: header.map((item) => ({
                                value: item.toLowerCase(), label: item
                            })), onChange: (value) => {
                                setColName(value);
                                // model?.trigger("vis_sql", value)
                                model === null || model === void 0 ? void 0 : model.set("vis_sql", [
                                    `select * EXCLUDE (index_rn1qaz2wsx)\nfrom \n(\nSELECT "${value}", ROW_NUMBER() OVER () AS index_rn1qaz2wsx\nFROM $$__NAME__$$\n)\nusing SAMPLE reservoir (500 rows) REPEATABLE(42)\norder by index_rn1qaz2wsx`,
                                    new Date().toISOString()
                                ]);
                                model === null || model === void 0 ? void 0 : model.save_changes();
                            } })))),
            react_1.default.createElement(core_1.Tabs.Panel, { value: "label" },
                react_1.default.createElement(core_1.Box, { h: "100%" })),
            react_1.default.createElement(core_1.Tabs.Panel, { value: "secondary" },
                react_1.default.createElement(core_1.Box, { h: "100%" })))));
};
const VisualPreviewChart = ({ rect, rect2, chartType, XAxis, colName }) => {
    const model = hooks_2.useModel();
    const [colData, setColData] = react_1.useState(model === null || model === void 0 ? void 0 : model.get("vis_data"));
    model === null || model === void 0 ? void 0 : model.on("change:vis_data", () => {
        setColData(model.get("vis_data"));
    });
    const lineData = colData ?
        JSON.parse(colData).data.map((item, index) => {
            return ({ a: index, b: item });
        })
        :
            [{ a: 0, b: 0 }];
    return (react_1.default.createElement(react_vega_1.VegaLite, { data: { values: lineData }, actions: false, spec: {
            width: rect.width - rect2.width - 32,
            height: rect2.height,
            params: [{
                    name: "industry",
                    select: { type: "point", fields: ["series"] },
                    bind: "legend"
                }],
            layer: [
                {
                    mark: chartType === 1 ? "line" : "bar",
                    transform: [
                        {
                            calculate: "datum.a", "as": XAxis,
                        },
                        {
                            calculate: "datum.b", "as": colName,
                        }
                    ],
                    encoding: {
                        x: { field: XAxis, type: "quantitative", axis: { tickMinStep: 30 } },
                        y: { field: colName, type: "quantitative" },
                        opacity: {
                            condition: { param: "industry", value: 1 },
                            value: 10
                        }
                    },
                    data: { name: 'values' } // note: vega-lite data attribute is a plain object instead of an array
                }
            ]
        } }));
};
const Visualization = () => {
    var _a;
    const model = hooks_2.useModel();
    const [hist, setHist] = react_1.useState((_a = model === null || model === void 0 ? void 0 : model.get("title_hist")) !== null && _a !== void 0 ? _a : "");
    model === null || model === void 0 ? void 0 : model.on("change:title_hist", () => { setHist(model.get("title_hist")); });
    const headerData = JSON.parse(hist !== null && hist !== void 0 ? hist : "{dtype:''}").filter((header) => header.dtype.includes("int") || header.dtype.includes("float")).map((header) => header.columnName);
    const quickName = JSON.parse((model === null || model === void 0 ? void 0 : model.get("vis_data")) !== "" ? model === null || model === void 0 ? void 0 : model.get("vis_data") : "{\"columns\":[]}").columns[0];
    const [colName, setColName] = react_1.useState(quickName === '' ? quickName : headerData[0]);
    const [XAxis, setXAxis] = react_1.useState("index");
    const [ref, rect] = hooks_1.useResizeObserver();
    const [ref2, rect2] = hooks_1.useResizeObserver();
    const [open, setOpen] = react_1.useState(true);
    const [chartType, setChartType] = react_1.useState(1);
    react_1.useEffect(() => {
        model === null || model === void 0 ? void 0 : model.trigger("vis_sql", colName);
    }, []);
    return (react_1.default.createElement(react_1.default.Fragment, null,
        react_1.default.createElement(core_1.Container, { ref: ref, fluid: true, sx: { padding: "1rem auto 2rem 1rem", margin: "auto 1rem auto 0rem", } },
            react_1.default.createElement(core_1.Group, { noWrap: true, sx: { gap: "0" } },
                react_1.default.createElement(core_1.Group, { ref: ref2, noWrap: true, sx: { height: 264, alignItems: "flex-start", gap: "0", paddingRight: "1rem" } },
                    open ?
                        react_1.default.createElement(VisualMenu, { chartType: chartType, setChartType: setChartType, setXAxis: setXAxis, setColName: setColName, colName: colName, header: headerData })
                        :
                            react_1.default.createElement(react_1.default.Fragment, null),
                    react_1.default.createElement(core_1.ActionIcon, { onClick: () => { setOpen(!open); } }, open ?
                        react_1.default.createElement(icons_react_1.IconChevronLeft, null)
                        :
                            react_1.default.createElement(icons_react_1.IconChevronRight, null)),
                    react_1.default.createElement(core_1.Divider, { orientation: "vertical" })),
                react_1.default.createElement(core_1.Stack, null,
                    react_1.default.createElement(VisualPreviewChart, { rect: rect, rect2: rect2, chartType: chartType, XAxis: XAxis, colName: colName }))))));
};
exports.Visualization = Visualization;
//# sourceMappingURL=visualization.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".custom-widget {\n  padding: 0px 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"asqlcell","version":"0.1.0","description":"Analytical sql cell for Jupyter","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/datarho/asqlcell","bugs":{"url":"https://github.com/datarho/asqlcell/issues"},"license":"BSD-3-Clause","author":{"name":"qizh","email":"qizh@datarho.tech"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/datarho/asqlcell"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf asqlcell/labextension","clean:nbextension":"rimraf asqlcell/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@emotion/react":"^11.10.5","@emotion/serialize":"^1.1.1","@emotion/utils":"^1.2.0","@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@mantine/core":"^5.10.0","@mantine/hooks":"^5.10.0","@tabler/icons-react":"^2.14.0","react":"^18.2.0","react-dom":"^17.0.2","react-icons":"^4.7.1","react-vega":"^7.6.0","vega":"^5.22.1","vega-lite":"^5.6.0"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@babel/preset-react":"^7.14.5","@babel/preset-typescript":"^7.14.5","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/react":"^17.0.11","@types/react-dom":"^17.0.8","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","babel-loader":"^8.2.2","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-plugin-react":"^7.31.11","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","jest-canvas-mock":"^2.4.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.61.0","webpack-cli":"^4.0.0"},"babel":{"presets":["@babel/preset-env","@babel/preset-react","@babel/preset-typescript"]},"jupyterlab":{"extension":"lib/plugin","outputDir":"asqlcell/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_WidgetModel_js.d8b9192b7996ffa07619.js.map