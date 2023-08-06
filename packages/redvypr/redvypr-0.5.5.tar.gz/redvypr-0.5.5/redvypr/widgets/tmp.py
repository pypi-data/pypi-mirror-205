#
#
#
class redvypr_dictionary_widget(QtWidgets.QWidget):
    """ Widget that lets the user interact with a configuration dictionary
    """

    def __init__(self, dictionary):
        """
        """
        funcname = __name__ + '.__init__():'
        super(QtWidgets.QWidget, self).__init__()
        self.setWindowIcon(QtGui.QIcon(_icon_file))
        self.dictionary = dictionary
        self.dictionary_local = copy.deepcopy(dictionary)
        logger.debug(funcname)
        self.layout = QtWidgets.QGridLayout(self)
        dictreewidget = redvypr_dictionary_tree(data=self.dictionary_local)
        self.layout.addWidget(dictreewidget)


class redvypr_qtreewidgetitem(QtWidgets.QTreeWidgetItem):
    """
    Custom QTreeWidgetItem class that keeps a record of the data
    dict
    list
    set (replace by list*?)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('Hallo!')

    def setText(self, *args, **kwargs):
        super().setText(*args, **kwargs)
        print('Text')

    def setData(self, *args, **kwargs):
        super().setData(*args, **kwargs)
        print('Data')


#
#
# LEGACY ?!?!?
#
#
class redvypr_dictionary_tree(QtWidgets.QTreeWidget):
    """ Qtreewidget that display and modifies the configuration of the calibration config
    """

    def __init__(self, data={}, dataname='data', editable=True):
        funcname = __name__ + '.__init__():'
        super().__init__()

        logger.debug(funcname + str(data))
        # make only the first column editable
        # self.setEditTriggers(self.NoEditTriggers)
        self.datatypes = [['int', int], ['float', float], ['str', str], ['list', list], ['dict', dict]]  # The datatypes
        self.datatypes_dict = {}  # Make a dictionary out of it, thats easier to reference
        for d in self.datatypes:
            self.datatypes_dict[d[0]] = d[1]
        self.header().setVisible(False)
        self.data = data
        self.dataname = dataname
        self.olddata = []
        self.numhistory = 100
        # Create the root item
        self.root = self.invisibleRootItem()
        # self.root.__data__ = data
        self.root.__dataindex__ = ''
        self.root.__datatypestr__ = ''
        self.root.__parent__ = None
        self.setColumnCount(3)
        self.create_qtree()
        print('Again check if update works')
        self.create_qtree()
        self.itemExpanded.connect(self.resize_view)
        self.itemCollapsed.connect(self.resize_view)
        # Connect edit triggers
        self.itemDoubleClicked.connect(self.checkEdit)
        self.itemChanged.connect(self.item_changed)  # If an item is changed
        self.currentItemChanged.connect(self.current_item_changed)  # If an item is changed

        # Connect the contextmenu
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menuContextTree)

    def rawcopy(self, data):
        """
        Functions that simply returns the input data, used as the basic field conversion function
        """
        return data

    def menuContextTree(self, point):
        # Infos about the node selected.
        index = self.indexAt(point)

        if not index.isValid():
            return

        item = self.itemAt(point)
        name = item.text(0)  # The text of the node.

        # We build the menu.
        datatype = item.__datatypestr__
        if ((datatype == 'list' or (datatype == 'dict'))):
            menu = QtWidgets.QMenu('Edit dict entry')
            action_add = menu.addAction("Add item")
            action_add.__item__ = item
            action_add.triggered.connect(self.add_rm_item_menu)
        else:
            menu = QtWidgets.QMenu('Edit dict entry')
            action_edit = menu.addAction("Edit item")
            action_edit.__item__ = item
            action_edit.triggered.connect(self.add_rm_item_menu)

        action_del = menu.addAction("Delete item")
        action_del.__item__ = item
        action_del.triggered.connect(self.add_rm_item_menu)
        menu.exec_(self.mapToGlobal(point))

    def seq_iter(self, obj):
        if isinstance(obj, dict):
            return obj
        elif isinstance(obj, list):
            return range(0, len(obj))
        else:
            return None

    def create_item(self, index, data, parent):
        """
        Creates recursively qtreewidgetitems. If the item to be created is a sequence (dict or list), it calls itself as often as it finds a real value
        Args:
            index:
            data:
            parent:

        Returns:

        """
        sequence = self.seq_iter(data)
        typestr = data.__class__.__name__
        if (sequence == None):  # Check if we have an item that is something with data (not a list or dict)
            item = QtWidgets.QTreeWidgetItem([str(index), str(data), typestr])
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)  # editable
            item.__data__ = data
            item.__dataindex__ = index
            item.__datatypestr__ = typestr
            item.__parent__ = parent
            index_child = self.item_is_child(parent, item)
            if index_child == None:  # Check if the item is already existing, if no add it
                parent.addChild(item)
            else:  # Update the data (even if it hasnt changed
                parent.child(index_child).setText(1, str(data))

        else:
            if (index is not None):
                indexstr = index
            newparent = QtWidgets.QTreeWidgetItem([str(index), '', typestr])
            newparent.__data__ = data
            newparent.__dataindex__ = index
            newparent.__datatypestr__ = typestr
            newparent.__parent__ = parent
            index_child = self.item_is_child(parent, newparent)
            if index_child == None:  # Check if the item is already existing, if no add it
                parent.addChild(newparent)
            else:
                newparent = parent.child(index_child)

            for newindex in sequence:
                newdata = data[newindex]
                self.create_item(newindex, newdata, newparent)

    def item_is_child(self, parent, child):
        """
        Checks if the item is a child already

        Args:
            parent:
            child:

        Returns:

        """
        numchilds = parent.childCount()
        # print('numchilds',numchilds,parent.text(0),parent)
        for i in range(numchilds):
            testchild = parent.child(i)
            # flag1 = testchild.__data__        == child.__data__
            flag1 = True
            flag2 = testchild.__dataindex__ == child.__dataindex__
            # flag3 = testchild.__datatypestr__ == child.__datatypestr__
            flag3 = True
            flag4 = testchild.__parent__ == child.__parent__

            # print('fdsfd',i,testchild.__data__,child.__data__)
            # print('flags',flag1,flag2,flag3,flag4)
            if (flag1 and flag2 and flag3 and flag4):
                # print('The same ...')
                return i

        return None

    def create_qtree(self, editable=True):
        """Creates a new qtree from the configuration and replaces the data in
        the dictionary with a configdata obejct, that save the data
        but also the qtreeitem, making it possible to have a synced
        config dictionary from/with a qtreewidgetitem. TODO: Worth to
        replace with a qviewitem?

        """
        funcname = __name__ + '.create_qtree():'
        logger.debug(funcname)
        self.blockSignals(True)
        if True:
            self.create_item(self.dataname, self.data, self.root)

        self.resizeColumnToContents(0)
        self.blockSignals(False)

    def checkEdit(self, item, column):
        """ Helper function that only allows to edit column 1
        """
        funcname = __name__ + '.checkEdit():'
        logger.debug(funcname + '{:d}'.format(column))

        if (column == 1) and (self.seq_iter(item.__data__) == None):
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)  # editable
        else:
            item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # not editable
            # self.edititem(item, column)

    def current_item_changed(self, current, previous):
        """ Save the data in the currently changed item, this is used to
        restore if newly entered data is not valid
        """
        # self.backup_data = current.text(1)
        item = current
        if (item is not None):
            if (item.parent() is not None):
                print(item.text(0), item.parent().text(0))

    def item_changed(self, item, column):
        """ Updates the dictionary with the changed data
        """
        funcname = __name__ + '.item_changed():'
        # logger.debug(funcname + 'Changed {:s} {:d} to {:s}'.format(item.text(0), column, item.text(1)))
        print(funcname + 'Changed {:s} {:d} to {:s}'.format(item.text(0), column, item.text(1)))

        index = item.__dataindex__
        datatypestr = item.__datatypestr__
        parentdata = item.__parent__.__data__
        newdatastr = item.text(1)
        self.change_dictionary(item, column, newdatastr, index, datatypestr, parentdata)
        self.resizeColumnToContents(0)

    def change_dictionary(self, item, column, newdatastr, index, datatypestr, parentdata):
        """
        Changes the dictionary
        Args:
            index:
            datatype:
            parentdata:

        Returns:

        """
        olddata = parentdata[index]

        convfunc = str
        for dtype in self.datatypes:
            if (datatypestr == dtype[0]):
                convfunc = dtype[1]

        print('Column', column)
        # Try to convert the new data, if not possible, except take the old data
        try:
            self.update_history()
            parentdata[index] = convfunc(newdatastr)
        except:
            item.setText(column, str(olddata))

    def update_history(self):
        """
        Manages the history of self.data by updating a list with a deepcopy of prior versions.

        Returns:

        """
        funcname = __name__ + 'update_history()'
        logger.debug(funcname)
        if (len(self.olddata) > self.numhistory):
            logger.debug('History overflow')
            self.olddata.pop(0)

        olddata = copy.deepcopy(self.data)
        self.olddata.append(olddata)  # Make a backup of the data

    def add_rm_item_menu(self):
        funcname = __name__ + 'add_rm_item_menu()'
        sender = self.sender()
        print('Sender', )
        item = sender.__item__
        if ('add' in sender.text().lower()):
            logger.debug(funcname + ' Adding item')
            self.add_item_widget(item)
        if ('edit' in sender.text().lower()):
            logger.debug(funcname + ' Editing item')
            self.add_item_widget(item)
        elif ('del' in sender.text().lower()):
            logger.debug(funcname + ' Deleting item')
            self.rm_item_widget(item)

    def rm_item_widget(self, item):
        """
        Remove item from qtreewidget and from self.data dictionary
        Args:
            item:

        Returns:

        """
        funcname = __name__ + 'rm_item_widget()'
        if True:  # Removing item
            index = item.__parent__.indexOfChild(item)
            # Remove from data
            if (item.__parent__ is not self.root):
                parentdata = item.__parent__.__data__
                parentdata.pop(item.__dataindex__)
                # Remove from qtreewidget
                item.__parent__.takeChild(index)
                print('data', self.data)

    def add_item_widget(self, item):
        """
        Widget for the user to add an item

        Returns:

        """
        self.__add_item_widget = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(self.__add_item_widget)
        self.__keyinput = QtWidgets.QLineEdit()
        self.__datainput = QtWidgets.QLineEdit()
        self.__datatypeinput = QtWidgets.QComboBox()
        listlist = ['list', 'dict']
        index_datatype = 0
        for i, d in enumerate(self.datatypes):
            if (item.__datatypestr__ == d[0]):
                index_datatype = i

            if (d[0] not in listlist):
                self.__datatypeinput.addItem(d[0])
            elif (item.__datatypestr__ in listlist):
                self.__datatypeinput.addItem(d[0])

        self.__datatypeinput.currentIndexChanged.connect(self.__combo_type_changed)
        self.__datatypeinput.__item__ = item
        self.__combo_type_changed()  # Grey out unnecessary input lines
        self.__apply = QtWidgets.QPushButton('Apply')
        self.__apply.__item__ = item
        self.__cancel = QtWidgets.QPushButton('Cancel')
        self.__apply.clicked.connect(self.__add_item_widget_click)
        self.__cancel.clicked.connect(self.__add_item_widget_click)
        layout.addRow(QtWidgets.QLabel('Key'), self.__keyinput)
        layout.addRow(QtWidgets.QLabel('Value'), self.__datainput)
        layout.addRow(QtWidgets.QLabel('Datatype'), self.__datatypeinput)
        layout.addRow(self.__apply, self.__cancel)
        self.__add_item_widget.show()

    def __combo_type_changed(self):
        datatype = self.__datatypeinput.currentText()
        item = self.__datatypeinput.__item__
        self.__keyinput.setEnabled(False)
        self.__datainput.setEnabled(True)
        parenttype = item.__parent__.__datatypestr__
        parenttype_list = (item.__parent__.__datatypestr__ == 'list')
        listlist = ['dict', 'list']
        datatype_item = item.__datatypestr__

        # Check if we have an item to edit, show the key
        if not (datatype_item in listlist):
            self.__keyinput.setText(str(item.__data__))
        # If an item is to be added to a dictionary, we need the key, otherwise not
        if (datatype_item == 'dict'):
            self.__keyinput.setEnabled(True)

    def __add_item_widget_click(self):
        sender = self.sender()
        funcname = __name__ + '__add_item_widget_click()'
        logger.debug(funcname)
        if (sender == self.__apply):
            logger.debug(funcname + ' Apply')
            item = sender.__item__
            newdata = self.__datainput.text()
            newdataindex = self.__keyinput.text()
            newdatatype = self.__datatypeinput.currentText()
            self.add_edit_item(item, newdata, newdataindex, newdatatype)
            print('Item', item)
        elif (sender == self.__cancel):
            logger.debug(funcname + ' Cancel')

        self.__add_item_widget.close()

    def add_edit_item(self, item, newdata, newdataindex, newdatatype):
        """
        Depending on the datatype of item either add newdata or modifies existing data
        Args:
            item:
            newdata:
            newdataindex:
            newdatatype:

        Returns:

        """
        funcname = __name__ + 'add_rm_item()'
        print('Hallo!', item)
        logger.debug(funcname + str(item.text(0)) + ' ' + str(item.text(1)))
        # Convert the text to the right format using the conversion function
        data = self.datatypes_dict[newdatatype](newdata)
        # Check how to append the data (depends on list or dict type of the item)
        if (item.__datatypestr__ == 'list'):
            logger.debug(funcname + ' Appending item to list')
            self.update_history()
            item.__data__.append(data)
            print('data', self.data)
            self.create_qtree()
        elif (item.__datatypestr__ == 'dict'):
            logger.debug(funcname + ' Adding item with key {:s} to dictionary'.format(newdataindex))
            self.update_history()
            item.__data__[newdataindex] = data
            print('data', self.data)
            self.create_qtree()
        else:
            print('Editing item', newdata, newdataindex, newdatatype)
            print('data before edit', self.data)
            index = item.__dataindex__
            item.__parent__.__data__[index] = newdata
            item.__datatypestr__ = newdatatype
            print('data edit', self.data)
            self.create_qtree()

    def resize_view(self):
        self.resizeColumnToContents(0)


#
#
# LEGACY?!?!
#
#
class redvypr_data_tree(QtWidgets.QTreeWidget):
    """ Qtreewidget that display a data structure
    """

    def __init__(self, data={}, dataname='data'):
        funcname = __name__ + '.__init__():'
        super().__init__()

        logger.debug(funcname + str(data))
        # make only the first column editable
        # self.setEditTriggers(self.NoEditTriggers)
        self.datatypes = [['int', int], ['float', float], ['str', str], ['list', list], ['dict', dict],
                          ['bool', bool]]  # The datatypes
        self.datatypes_dict = {}  # Make a dictionary out of it, thats easier to reference
        for d in self.datatypes:
            self.datatypes_dict[d[0]] = d[1]
        self.header().setVisible(False)
        self.data = data
        self.dataname = dataname
        # Create the root item
        self.root = self.invisibleRootItem()
        # self.root.__data__ = data
        self.root.__dataindex__ = ''
        self.root.__datatypestr__ = ''
        self.root.__parent__ = None
        self.setColumnCount(3)
        self.create_qtree()
        self.itemExpanded.connect(self.resize_view)
        self.itemCollapsed.connect(self.resize_view)

    def rawcopy(self, data):
        """
        Functions that simply returns the input data, used as the basic field conversion function
        """
        return data

    def seq_iter(self, obj):
        if isinstance(obj, dict):
            return obj
        elif isinstance(obj, list):
            return range(0, len(obj))
        else:
            return None

    def create_item(self, index, data, parent):
        """
        Creates recursively qtreewidgetitems. If the item to be created is a sequence (dict or list), it calls itself as often as it finds a real value
        Args:
            index:
            data:
            parent:

        Returns:

        """
        sequence = self.seq_iter(data)
        typestr = data.__class__.__name__
        if (sequence == None):  # Check if we have an item that is something with data (not a list or dict)
            item = QtWidgets.QTreeWidgetItem([str(index), str(data), typestr])
            item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)  # editable
            item.__data__ = data
            item.__dataindex__ = index
            item.__datatypestr__ = typestr
            item.__parent__ = parent
            index_child = self.item_is_child(parent, item)
            if index_child == None:  # Check if the item is already existing, if no add it
                parent.addChild(item)
            else:  # Update the data (even if it hasnt changed
                parent.child(index_child).setText(1, str(data))

        else:
            if (index is not None):
                indexstr = index
            newparent = QtWidgets.QTreeWidgetItem([str(index), '', typestr])
            item = newparent
            newparent.__data__ = data
            newparent.__dataindex__ = index
            newparent.__datatypestr__ = typestr
            newparent.__parent__ = parent
            index_child = self.item_is_child(parent, newparent)
            if index_child == None:  # Check if the item is already existing, if no add it
                parent.addChild(newparent)
            else:
                newparent = parent.child(index_child)

            for newindex in sequence:
                newdata = data[newindex]
                self.create_item(newindex, newdata, newparent)

    def item_is_child(self, parent, child):
        """
        Checks if the item is a child already

        Args:
            parent:
            child:

        Returns:

        """
        numchilds = parent.childCount()
        for i in range(numchilds):
            testchild = parent.child(i)
            # flag1 = testchild.__data__        == child.__data__
            flag1 = True
            flag2 = testchild.__dataindex__ == child.__dataindex__
            # flag3 = testchild.__datatypestr__ == child.__datatypestr__
            flag3 = True
            flag4 = testchild.__parent__ == child.__parent__

            # print('fdsfd',i,testchild.__data__,child.__data__)
            # print('flags',flag1,flag2,flag3,flag4)
            if (flag1 and flag2 and flag3 and flag4):
                return i

        return None

    def create_qtree(self, editable=True):
        """Creates a new qtree from the configuration and replaces the data in
        the dictionary with a configdata obejct, that save the data
        but also the qtreeitem, making it possible to have a synced
        config dictionary from/with a qtreewidgetitem. TODO: Worth to
        replace with a qviewitem?

        """
        funcname = __name__ + '.create_qtree():'
        logger.debug(funcname)
        self.blockSignals(True)
        if True:
            self.create_item(self.dataname, self.data, self.root)

        self.dataitem = self.root.child(0)
        self.resizeColumnToContents(0)
        self.blockSignals(False)

    def resize_view(self):
        self.resizeColumnToContents(0)



#
#
#
#
#
class redvypr_config_widget(QtWidgets.QWidget):
    config_changed = QtCore.pyqtSignal(dict)  # Signal notifying that the configuration has changed
    config_changed_flag = QtCore.pyqtSignal()  # Signal notifying that the configuration has changed
    def __init__(self, template={}, config=None,loadsavebutton=True,redvypr_instance=None):
        funcname = __name__ + '.__init__():'
        super().__init__()
        self.redvypr=redvypr_instance
        # TODO, convert config to dictionary with configdata objects
        self.config = config
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setColumnStretch(0, 1)
        self.layout.setColumnStretch(1, 1)
        try:
            configname = config['name']
        except:
            configname = 'config'

        self.template = template
        conftemplate = configtemplate_to_dict(template=template)
        if(config is not None):
            logger.debug(funcname + 'Applying config to template')
            self.config = redvypr.configdata.apply_config_to_dict(config, conftemplate)

        self.configtree = redvypr_config_tree(data = self.config,dataname=configname)
        self.configtree.expandAll()
        self.configtree.resizeColumnToContents(0)

        #self.itemExpanded.connect(self.resize_view)
        #self.itemCollapsed.connect(self.resize_view)
        self.configtree.itemDoubleClicked.connect(self.__open_config_gui)
        #self.configtree.itemChanged.connect(self.item_changed)  # If an item is changed
        #self.configtree.currentItemChanged.connect(self.current_item_changed)  # If an item is changed
        self.configgui = QtWidgets.QWidget() # Widget where the user can modify the content
        self.configgui_layout = QtWidgets.QVBoxLayout(self.configgui)

        if(loadsavebutton):
            # Add load/save buttons
            self.load_button = QtWidgets.QPushButton('Load')
            self.load_button.clicked.connect(self.load_config)
            self.save_button = QtWidgets.QPushButton('Save')
            self.save_button.clicked.connect(self.save_config)

        self.layout.addWidget(self.configtree,0,0)
        self.layout.addWidget(self.configgui, 0, 1)
        if (loadsavebutton):
            self.layout.addWidget(self.load_button, 1, 0)
            self.layout.addWidget(self.save_button, 1, 1)

    def reload_config(self):
        """
        Clears the configtree and redraws it. Good after a third person change of the configuration
        Returns:

        """
        funcname = __name__ + '.reload_config():'
        logger.debug(funcname)
        self.configtree.reload_data(self.config)

    def load_config(self):
        funcname = __name__ + '.load_config():'
        fname_open = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '',"YAML files (*.yaml);; All files (*)")
        if(len(fname_open[0]) > 0):
            logger.info(funcname + 'Opening file {:s}'.format(fname_open[0]))
            fname = fname_open[0]
            with open(fname, 'r') as yfile:
                config = yaml.safe_load(yfile)
                conftemplate = configtemplate_to_dict(template=self.template)
                if (config is not None):
                    logger.debug(funcname + 'Applying config to template')
                    self.config = redvypr.configdata.apply_config_to_dict(config, conftemplate)
                    print('New config:',config)
                    self.reload_config()


    def save_config(self):
        funcname = __name__ + '.save_config():'
        fname_open = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', '',"YAML files (*.yaml);; All files (*)")
        if(len(fname_open[0]) > 0):
            logger.info(funcname + 'Save file file {:s}'.format(fname_open[0]))
            print('Saving', self.configtree.data)
            config = copy.deepcopy(self.configtree.data)
            print('Deepcopy', config)
            fname = fname_open[0]
            with open(fname, 'w') as yfile:
                yaml.dump(config, yfile)

    def get_config(self):
        """
        Returns a configuation dictionary of the qtreewidgetitem

        Returns:

        """
        config = copy.deepcopy(self.configtree.data)
        return config


    def __open_config_gui(self,item):
        """
        After an item was clicked this function checks if there is a configuration gui for that type of data, if yes open that configuration
        widget
        Returns:

        """
        funcname = __name__ + '.__open_config_gui():'
        data = item.__data__
        try:
            options = item.__options__
        except:
            options = None

        try:
            modifiable = item.__modifiable__
        except:
            modifiable = False

        try:
            modifiable_parent = item.__parent__.__modifiable__
        except:
            modifiable_parent = False
        print(funcname, type(data),modifiable,modifiable_parent)

        if (type(data) == dict) and modifiable_parent: # A template dictionary item in a modifiable list
            pass
        elif((type(data) == list) or (type(data) == dict)) and not(modifiable):
            return

        try:
            dtype = data.template['type']
        except:
            if(type(data) == redvypr.configdata.configdata):
                dtype = data.value.__class__.__name__
            else:
                dtype = data.__class__.__name__

            #print('dtpye',dtype)
            #dtype = 'str'

        item.__datatype__ = dtype
        self.remove_input_widgets()
        if (dtype == 'dict'):
            #print('Dictdictdict')
            self.config_widget_dict(item)
        elif(dtype == 'int'):
            self.config_widget_number(item,'int')
        elif (dtype == 'float'):
            self.config_widget_number(item,'float')
        elif (dtype == 'datastream'):
            self.config_widget_datastream(item)
        elif (dtype == 'color'):
            self.config_widget_color(item)
        elif (dtype == 'bool'):
            #
            data.template['options'] = ['False','True']
            self.config_widget_str_combo(item)
        elif(dtype == 'str'):
            # If we have options
            try:
                data.template['options']
                self.config_widget_str_combo(item)
            # Let the user enter
            except Exception as e:
                print('Exception',e)
                self.config_widget_str(item)
        elif (dtype == 'list'): # Modifiable list
            self.config_widget_list_combo(item)
            #print('List')


    def __config_widget_button(self):
        """
        Applies the changes of the configuration widget

        Returns:

        """
        funcname = __name__ + '.__config_widget_button(): '
        btn = self.sender()
        if(btn == self.__configwidget_apply):
            item = btn.item
            dtype = item.__datatype__
            logger.debug(funcname + 'Apply')
            data = None
            btntext = btn.text()
            try:
                flag_remove = btn.__removeitem__
            except:
                flag_remove = False
            #print('btntext',btntext)
            if (flag_remove):  # Add/Remove from list
                logger.debug(funcname + ' Removing item')
                item.__dataparent__.remove(item.__data__)
                self.reload_config()
                config = self.get_config()
                self.config_changed_flag.emit()
                self.config_changed.emit(config)
                return
            if (dtype == 'list'):  # Add/Remove from list
                #print('Add to list')
                templatename = str(self.__configwidget_input.currentText())
                template_options = item.__options__
                template_names = []
                newitem_dict = redvypr.configdata.configdata(None)
                for t in template_options:
                    if(templatename == t['template_name']):
                        #print('Found template')
                        configdict = redvypr.configdata.configtemplate_to_dict(t)
                        newitem_dict = configdict

                #print('tname',templatename)
                template = item.__dataparent__[item.__dataindex__].template
                #print('Template')
                item.__dataparent__[item.__dataindex__].value.append(newitem_dict)
                #print(item.__dataparent__[item.__dataindex__])
                self.reload_config()
                config = self.get_config()
                self.config_changed_flag.emit()
                self.config_changed.emit(config)
                return

            elif (dtype == 'datastream'):
                data = self.__configwidget_input.datastreamcustom.text()

            elif (dtype == 'color'):
                color = self.__configwidget_input.currentColor()
                rgb = color.getRgb()
                data = list(rgb)

            # TODO, check what kind of widget we have here
            if (data is None):
                try:
                    data = self.__configwidget_input.value() # Works for int/float spinboxes
                except:
                    pass

            if (data is None):
                try:
                    data = self.__configwidget_input.text() # Works for lineedits (str)
                except:
                    pass
            if (data is None):
                try:
                    data = str(self.__configwidget_input.currentText()) # Works for comboboxes (combo_str)
                except Exception as e:
                    pass

                #print('DATADATATAT',data,type(data),dtype,bool(data))
                # Test if we have a bool
                if(dtype == 'bool'):
                    data = data.lower() == 'True'

            if(data is not None):
                logger.debug(funcname + 'Got data')
                print('data',data)
                item.setText(1,str(data))
                try: # If configdata
                    item.__dataparent__[item.__dataindex__].value = data
                except:
                    item.__dataparent__[item.__dataindex__] = data
            else:
                logger.debug(funcname + 'No valid data')

        config = self.get_config()
        self.config_changed_flag.emit()
        self.config_changed.emit(config)

    def config_widget_color(self, item):
        """
                Lets the user choose a color
                Args:
                    item:

                Returns:

                """
        self.remove_input_widgets()

        self.__configwidget_int = QtWidgets.QWidget()
        self.__layoutwidget_int = QtWidgets.QVBoxLayout(self.__configwidget_int)
        # The color dialog
        colorwidget = QtWidgets.QColorDialog(self.__configwidget_int)
        colorwidget.setOptions(QtWidgets.QColorDialog.NoButtons| QtWidgets.QColorDialog.DontUseNativeDialog)
        colorwidget.setWindowFlags(QtCore.Qt.Widget)
        self.__configwidget_input = colorwidget
        self.__layoutwidget_int.addWidget(colorwidget)
        # Buttons
        self.__configwidget_apply = QtWidgets.QPushButton('Apply')
        self.__configwidget_apply.clicked.connect(self.__config_widget_button)
        self.__configwidget_apply.item = item
        self.configgui_layout.addWidget(self.__configwidget_int)
        self.__layoutwidget_int.addWidget(self.__configwidget_apply)
        colorwidget.open()
        #self.__layoutwidget_int.addWidget(self.w)

    def config_widget_datastream(self, item):
        """
        Lets the user change a datastream
        Args:
            item:

        Returns:

        """
        self.remove_input_widgets()
        datastreamwidget = redvypr_devicelist_widget(redvypr=self.redvypr, showapplybutton=False)
        datastreamwidget.item     = item
        self.__configwidget_input = datastreamwidget
        self.__configwidget_int   = QtWidgets.QWidget()
        self.__layoutwidget_int   = QtWidgets.QFormLayout(self.__configwidget_int)
        self.__layoutwidget_int.addRow(datastreamwidget)
        # Buttons
        self.__configwidget_apply = QtWidgets.QPushButton('Apply')
        self.__configwidget_apply.clicked.connect(self.__config_widget_button)
        self.__configwidget_apply.item = item
        self.configgui_layout.addWidget(self.__configwidget_int)
        self.__layoutwidget_int.addRow(self.__configwidget_apply)

    def config_widget_number(self, item, dtype='int'):
        """
        Creates a widgets to modify an integer value

        Returns:

        """
        index = item.__dataindex__
        self.__configwidget_int = QtWidgets.QWidget()
        self.__layoutwidget_int = QtWidgets.QFormLayout(self.__configwidget_int)
        #self.__configwidget_input = QtWidgets.QLineEdit()
        if(dtype=='int'):
            self.__configwidget_input = QtWidgets.QSpinBox()
            self.__configwidget_input.setRange(int(-1e9),int(1e9))
            try:
                value = int(item.text(1))
            except:
                value = 0
            self.__configwidget_input.setValue(value)
        else:
            self.__configwidget_input = QtWidgets.QDoubleSpinBox()
            self.__configwidget_input.setRange(-1e9, 1e9)
            try:
                value = float(item.text(1))
            except:
                value = 0.0
            self.__configwidget_input.setValue(value)

        self.__layoutwidget_int.addRow(QtWidgets.QLabel('Enter value for {:s}'.format(index)))
        self.__layoutwidget_int.addRow(QtWidgets.QLabel('Value'), self.__configwidget_input)
        # Buttons
        self.__configwidget_apply = QtWidgets.QPushButton('Apply')
        self.__configwidget_apply.clicked.connect(self.__config_widget_button)
        self.__configwidget_apply.item = item
        self.__layoutwidget_int.addRow(self.__configwidget_apply)
        self.configgui_layout.addWidget(self.__configwidget_int)

    def config_widget_str(self,item):

        index = item.__dataindex__
        data = ''
        try:
            data = str(item.__data__)
        except:
            pass
        try:
            data = str(item.__data__.value)
        except:
            pass

        self.remove_input_widgets()
        self.__configwidget_int = QtWidgets.QWidget()
        self.__layoutwidget_int = QtWidgets.QFormLayout(self.__configwidget_int)
        self.__configwidget_input = QtWidgets.QLineEdit()
        self.__configwidget_input.setText(data)
        self.__layoutwidget_int.addRow(QtWidgets.QLabel('Enter string for {:s}'.format(index)))
        self.__layoutwidget_int.addRow(QtWidgets.QLabel('Value'), self.__configwidget_input)
        # Buttons
        self.__configwidget_apply = QtWidgets.QPushButton('Apply')
        self.__configwidget_apply.clicked.connect(self.__config_widget_button)
        self.__configwidget_apply.item = item
        self.configgui_layout.addWidget(self.__configwidget_int)
        self.__layoutwidget_int.addRow(self.__configwidget_apply)


    def config_widget_str_combo(self, item):
        index = item.__dataindex__
        data  = item.__data__
        options = data.template['options']
        self.remove_input_widgets()
        self.__configwidget_int = QtWidgets.QWidget()
        self.__layoutwidget_int = QtWidgets.QFormLayout(self.__configwidget_int)
        self.__configwidget_input = QtWidgets.QComboBox()
        for option in options:
            self.__configwidget_input.addItem(option)
        self.__layoutwidget_int.addRow(QtWidgets.QLabel('Options for {:s}'.format(index)))
        self.__layoutwidget_int.addRow(QtWidgets.QLabel('Value'), self.__configwidget_input)
        # Buttons
        self.__configwidget_apply = QtWidgets.QPushButton('Apply')
        self.__configwidget_apply.clicked.connect(self.__config_widget_button)
        self.__configwidget_apply.item = item
        self.configgui_layout.addWidget(self.__configwidget_int)
        self.__layoutwidget_int.addRow(self.__configwidget_apply)

    def config_widget_list_combo(self, item):
        """
        Config widget for a modifiable list
        Args:
            item:

        Returns:

        """
        index = item.__dataindex__
        data = item.__data__
        template_options = item.__options__
        options = []
        for t in template_options:
            options.append(t['template_name'])
        print('Options',options)
        self.remove_input_widgets()
        self.__configwidget_int = QtWidgets.QWidget()
        self.__layoutwidget_int = QtWidgets.QFormLayout(self.__configwidget_int)
        self.__configwidget_input = QtWidgets.QComboBox()
        for option in options:
            self.__configwidget_input.addItem(option)
        self.__layoutwidget_int.addRow(QtWidgets.QLabel('Options for {:s}'.format(index)))
        self.__layoutwidget_int.addRow(QtWidgets.QLabel('Value'), self.__configwidget_input)
        # Buttons
        self.__configwidget_apply = QtWidgets.QPushButton('Add')
        self.__configwidget_apply.clicked.connect(self.__config_widget_button)
        self.__configwidget_apply.item = item
        self.configgui_layout.addWidget(self.__configwidget_int)
        self.__layoutwidget_int.addRow(self.__configwidget_apply)


    def config_widget_dict(self, item):
        """
        Config widget to edit (at the moment remove) a dictionary item
        Args:
            item:

        Returns:

        """

        funcname = __name__ + '.config_widget_dict(): '
        logger.debug(funcname)
        index = item.__dataindex__
        data  = item.__data__
        self.remove_input_widgets()
        self.__configwidget_int = QtWidgets.QWidget()
        self.__layoutwidget_int = QtWidgets.QFormLayout(self.__configwidget_int)
        # Buttons
        self.__configwidget_apply = QtWidgets.QPushButton('Remove')
        self.__configwidget_apply.clicked.connect(self.__config_widget_button)
        self.__configwidget_apply.item = item
        self.__configwidget_apply.__removeitem__ = True
        self.configgui_layout.addWidget(self.__configwidget_int)
        self.__layoutwidget_int.addRow(self.__configwidget_apply)


    def remove_input_widgets(self):
        """
        Removes all widgets from configgui
        Returns:

        """
        layout = self.configgui_layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        #for i in range(len(self.__configgui_list)):
        #    widget = self.__configgui_list.pop()
        #    self.configgui_layout.remWidget(widget)

#
#
#
#
#
class redvypr_config_tree(QtWidgets.QTreeWidget):
    """ Qtreewidget that display a data structure
    """

    def __init__(self, data={}, dataname='data'):
        funcname = __name__ + '.__init__():'
        super().__init__()

        logger.debug(funcname + str(data))
        self.setExpandsOnDoubleClick(False)
        # make only the first column editable
        #self.setEditTriggers(self.NoEditTriggers)
        #self.header().setVisible(False)
        self.setHeaderLabels(['Variable','Value','Type'])
        self.data     = data
        self.dataname = dataname
        # Create the root item
        self.root = self.invisibleRootItem()
        #self.root.__data__ = data
        self.root.__dataindex__ = ''
        self.root.__datatypestr__ = ''
        self.root.__parent__ = None
        self.setColumnCount(3)
        self.create_qtree()
        #self.itemExpanded.connect(self.resize_view)
        #self.itemCollapsed.connect(self.resize_view)

    def reload_data(self,data):
        self.data = data
        self.clear()
        self.create_qtree()
        self.expandAll()
        self.resizeColumnToContents(0)

    def seq_iter(self,obj):
        return redvypr.configdata.seq_iter(obj)

    def create_item(self, index, data, parent):
        """
        Creates recursively qtreewidgetitems. If the item to be created is a sequence (dict or list), it calls itself as often as it finds a real value
        Args:
            index:
            data:
            parent:

        Returns:

        """
       # print('data0',data)
        try:
            sequence = self.seq_iter(data.value)
        except:
            sequence = self.seq_iter(data)
        #print('Data',sequence)
        if(sequence == None): # Check if we have an item that is something with data (not a list or dict)
            data_value = data.value  # Data is a configdata object, or list or dict
            #print('Data value',str(data_value),data)
            flag_configdata = False
            try:
                typestr = data.template['type']
                flag_configdata = True
            except:
                typestr = data_value.__class__.__name__


            item       = QtWidgets.QTreeWidgetItem([str(index), str(data_value),typestr])
            #item.setFlags(item.flags() | QtCore.Qt.ItemIsEditable)  # editable
            item.__data__ = data
            item.__dataparent__   = parent.__data__ # can be used to reference the data (and change it)
            item.__dataindex__    = index
            item.__datatypestr__  = typestr
            item.__parent__       = parent

            index_child = self.item_is_child(parent, item)
            if  index_child == None:  # Check if the item is already existing, if no add it
                parent.addChild(item)
            else: # Update the data (even if it hasnt changed
                parent.child(index_child).setText(1,str(data_value))

        else:
            #print('loop')
            try:
                datatmp = data.value
            except:
                datatmp = data


            typestr = datatmp.__class__.__name__
            flag_modifiable = False
            try:
                options = data.template['options'] # Modifiable list (configdata with value "list")
                flag_modifiable = True
            except:
                options = None

            if(index is not None):
                indexstr = index
            newparent = QtWidgets.QTreeWidgetItem([str(index), '',typestr])
            item = newparent
            newparent.__data__         = datatmp
            newparent.__dataindex__    = index
            newparent.__datatypestr__  = typestr
            newparent.__parent__       = parent
            newparent.__modifiable__   = flag_modifiable
            try:
                newparent.__dataparent__ = parent.__data__  # can be used to reference the data (and change it)
            except:
                newparent.__dataparent__ = None
            if (options is not None):  # Modifiable list
                #print('List item, adding options')
                newparent.__options__ = options



            index_child = self.item_is_child(parent, newparent)
            if index_child == None:  # Check if the item is already existing, if no add it
                parent.addChild(newparent)
            else:
                newparent = parent.child(index_child)

            for newindex in sequence:
                newdata = datatmp[newindex]
                self.create_item(newindex,newdata,newparent)

    def item_is_child(self,parent,child):
        """
        Checks if the item is a child already

        Args:
            parent:
            child:

        Returns:

        """
        numchilds  = parent.childCount()
        for i in range(numchilds):
            testchild = parent.child(i)
            #flag1 = testchild.__data__        == child.__data__
            flag1 = True
            flag2 = testchild.__dataindex__   == child.__dataindex__
            #flag3 = testchild.__datatypestr__ == child.__datatypestr__
            flag3 = True
            flag4 = testchild.__parent__      == child.__parent__

            #print('fdsfd',i,testchild.__data__,child.__data__)
            #print('flags',flag1,flag2,flag3,flag4)
            if(flag1 and flag2 and flag3 and flag4):
                return i

        return None

    def create_qtree(self, editable=True):
        """Creates a new qtree from the configuration and replaces the data in
        the dictionary with a configdata obejct, that save the data
        but also the qtreeitem, making it possible to have a synced
        config dictionary from/with a qtreewidgetitem. TODO: Worth to
        replace with a qviewitem?

        """
        funcname = __name__ + '.create_qtree():'
        logger.debug(funcname)
        self.blockSignals(True)
        if True:
            self.create_item(self.dataname,self.data,self.root)

        self.dataitem = self.root.child(0)
        self.resizeColumnToContents(0)
        self.blockSignals(False)

    def resize_view(self):
        pass
        print('resize ...')
        #self.resizeColumnToContents(0)



def apply_config_to_configDict(userconfig,configdict):
    """
    Applies a user configuration to a dictionary created from a template
    Args:
        userconfig:
        configdict:

    Returns:
        configdict_applied: A with the userconfig modified configuration dictionary
    """
    funcname = __name__ + '.apply_config_to_configDict():'
    def loop_over_index(c,cuser):
        for index in seq_iter(cuser): # Loop over the user config
            #print('Hallo',index,getdata(c[index]))
            #print('c', c, index)
            indices = seq_iter(c)
            #print('c', c, index,indices)
            #print(index in indices)
            # Try to get the same index in the template
            try:
                ctemp = c[index]
            except:
                try:
                    ctemp = c.value[index]
                except: # Could not get data, forget the index and continue with next one
                    continue


            if (seq_iter(ctemp) is not None):
                #print('Hallo',cuser,index)
                try: # Check if the user data is existing as well
                    cuser[index]
                    if (seq_iter(cuser[index]) is not None):
                        loop_over_index(ctemp, cuser[index])
                except Exception as e:
                    logger.debug(funcname + ': cuser[index]: ' + str(e))
                    continue


            # Check if this is a configdata list, that can be modified
            elif(type(getdata(ctemp)) == list):
                try:
                    t = ctemp.template['type']
                except Exception as e:
                    t = ''

                if(t == 'list'): # modifiable list, fill the template list with the types
                    # First make the list equally long, the user list is either 0 or longer
                    numitems = len(getdata(cuser[index]))
                    dn = numitems - len(ctemp.value)
                    for i in range(dn):
                        ctemp.value.append(configdata(None))

                    # Fill the list with the right templates
                    for i in range(numitems):
                        try:
                            nameuser = getdata(cuser[index][i]['template_name'])
                        except:
                            nameuser = ''

                        FLAG_FOUND_VALID_OPTION = False
                        for o in ctemp.template['options']:
                            nameoption = o['template_name']
                            if(nameoption == nameuser):
                                ctemp.value[i] = configtemplate_to_dict(o)
                                FLAG_FOUND_VALID_OPTION = True
                                break

                        if(FLAG_FOUND_VALID_OPTION == False):
                            cuser[index][i] = None

                    # Loop again
                    loop_over_index(ctemp, cuser[index])

            else: # Apply the value
                try:
                    ctemp = c.value # If c is a configdata with a list (used for modifiable list)
                except:
                    ctemp = c

                try:  # Check if the user data is existing as well
                    ctemp[index].value = cuser[index]
                except: # Is this needed anymore? Everything should be configdata ...
                    try:  # Check if the user data is existing as well
                        ctemp[index] = cuser[index]
                    except:
                        pass
                    pass

    #print('Configdict before:', configdict)
    loop_over_index(configdict,userconfig)
    #print('Configdict after:', configdict)
    return configdict



#
# Legacy, replaced by dict_to_configDict(process_template=True)
#
def template_to_configDict(template):
    """
    creates a config dictionary out of a configuration template, the values of the dictionary are
    configList/configNumber objects that can be accessed like classical values but have the capability to store
    attributes as well.

    """
    funcname = __name__ + 'template_to_config():'
    def loop_over_index(c):
        print('c',c,seq_iter(c))
        print(type(c))
        for index in seq_iter(c):
            print('c1', c[index])
            c[index] = data_to_configdata(c[index]) # Brute conversion of everything
            print('c2', c[index])
            # Check first if we have a configuration dictionary with at least the type
            FLAG_CONFIG_DICT = False
            if(type(c[index]) == dict):
                if ('default' in c[index].keys()):
                    default_value = c[index]['default']
                    default_type = default_value.__class__.__name__ # Defaults overrides type
                    FLAG_CONFIG_DICT = True
                if('type' in c[index].keys()):
                    default_type = c[index]['type']
                    default_value = ''
                    FLAG_CONFIG_DICT = True
                    if(c[index]['type'] == 'list'): # Modifiable list
                        #print('List')
                        if ('default' in c[index].keys()): # The default values are templates and need to be converted to dicts
                            default_value_tmp = c[index]['default']
                            default_value = []
                            if (type(default_value_tmp) == list):
                                for d in default_value_tmp:
                                    if(valid_template(d)):
                                        default_value.append(template_to_configDict(d))
                                    else:
                                        raise TypeError("The list entry should be a valid redvypr template")


                            else:
                                raise TypeError("The default value should be a list containing templates")
                        else:
                            default_value = []


            # Iterate over a dictionary or list
            if ((seq_iter(c[index]) is not None) and (FLAG_CONFIG_DICT == False)):
                #print('Loop')
                loop_over_index(c[index])
            else:
                # Check if we have some default values like type etc ...
                try:
                    confdata = data_to_configdata(default_value) # Configdata object
                    confdata.template = c[index]
                    c[index] = confdata
                except Exception as e:
                    #print('Exception',e)
                    confdata = data_to_configdata(c[index])
                    confdata.template = c[index]
                    c[index] = confdata


    config_tmp = copy.deepcopy(template) # Copy the template first
    if(type(config_tmp) == dict):
        config = configDict(template) #
    else:
        raise TypeError(funcname + 'template must be a dictionary and not {:s}'.format(str(type(template))))
    loop_over_index(config)
    #print('Config:',config)
    return config









