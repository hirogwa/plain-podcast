/*
  Simple input form with caption
*/
var TextInput = React.createClass({
    render: function() {
        var caption = React.createElement(
            'h3', {ref: 'caption'}, this.props.caption
        );

        var textInput = React.createElement(
            'input', {ref: 'text', placeholder: this.props.placeholder}
        );

        return React.createElement(
            'div', {className: 'textInput'},
            [caption, textInput]
        );
    }
});

/*
  Text input form with character limit.
  Character count is displayed max->0 as characters are typed.
*/
var CharacterCountRestrictionTextarea = React.createClass({
    getInitialState: function() {
        return {text: ""};
    },

    handleInput: function(e) {
        e.preventDefault();
        this.setState({text: this.refs.text.getDOMNode().value});
        return;
    },

    render: function() {
        var caption = React.createElement(
            'h3', { ref: 'caption' }, this.props.caption
        );

        var textform = React.createElement(
            'textarea',
            { ref: 'text',
              placeholder: this.props.placeholder,
              onChange: this.handleInput,
              value: this.state.text}
        );

        var countClass = this.props.maxcount < this.state.text.length
                ? "overlimit" : "withinlimit";
        var characterCount = React.createElement(
            'p',
            { className: countClass },
            (this.props.maxcount - this.state.text.length).toString()
                + ' characters remaining');

        return React.createElement(
            'div', {className: 'characterCountRestrictionForm'},
            [caption, textform, characterCount]);
    }
});

/*
  Set of components used to add a text to a list.
  The text is optionally associated with a link.
*/
var LinkedTextItemAdder = React.createClass({
    getInitialState: function() {
        return {
            addable: false
        };
    },

    getDefaultProps: function() {
        return {
            textplaceholder: 'text',
            urlplaceholder: 'url',
        };
    },

    handleKeyUpText: function(e) {
        var url = this.refs.url.getDOMNode().value.trim();
        this.setState({addable: url});

        if (e.keyCode == 13 && this.state.addable) {
            this.props.addItemCallback();
        }
    },

    handleKeyUpUrl: function(e) {
        var url = this.refs.url.getDOMNode().value.trim();
        this.setState({addable: url});

        if (e.keyCode == 13 && this.state.addable) {
            this.props.addItemCallback();
        }
    },

    handleClickAdd: function(e) {
        if (this.state.addable) {
            this.props.addItemCallback();
        }
    },

    render: function() {
        var textinput = React.createElement(
            'input',
            {ref: 'text',
             onKeyUp: this.handleKeyUpText,
             placeholder: this.props.textplaceholder
            }
        );

        var urlinput = React.createElement(
            'input',
            {ref: 'url',
             onKeyUp: this.handleKeyUpUrl,
             placeholder: this.props.urlplaceholder
            }
        );

        var addbutton = React.createElement(
            'button', {
                ref: 'addbutton',
                disabled: !this.state.addable,
                onClick: this.handleClickAdd
            },
            'add'
        );

        return React.createElement(
            'div', {className: 'linkedTextItemAdder'},
            [textinput, urlinput, addbutton]
        );
    }
});

/*
  One text item after added, on view mode.
*/
var LinkedTextItemForView = React.createClass({
    onRemove: function(e) {
        e.preventDefault();
        this.props.removeItemCallback();
    },

    onEdit: function(e) {
        e.preventDefault();
        this.props.editItemCallback();
    },

    render: function() {
        var text = React.createElement(
            'a', {ref: 'linkedText',
                  className: 'linkedText',
                  href: this.props.url,
                  target: '_blank'
                 },
            this.props.text
        );
        var editbutton = React.createElement(
            'button', {
                ref: 'editbutton',
                onClick: this.onEdit,
            },
            'edit'
        );
        var removebutton = React.createElement(
            'button', {
                ref: 'removebutton',
                onClick: this.onRemove,
            },
            'remove'
        );
        return React.createElement(
            'div', {className: 'linkedTextItemForView'},
            [text, editbutton, removebutton]
        );
    }
});

/*
  One text item after added, on edit mode.
*/
var LinkedTextItemForEdit = React.createClass({
    componentDidMount: function() {
        this.refs.text.getDOMNode().select();
    },

    getInitialState: function() {
        return {
            commitable: true
        };
    },

    handleKeyDownText: function(e) {
        var url = this.refs.url.getDOMNode().value.trim();
        this.setState({commitable: url});

        if (e.keyCode == 13 && this.state.commitable) {
            this.props.commitItemCallback(this);
        }
    },

    handleKeyDownUrl: function(e) {
        var url = this.refs.url.getDOMNode().value.trim();
        this.setState({commitable: url});

        if (e.keyCode == 13 && this.state.commitable) {
            this.props.commitItemCallback(this);
        }
    },

    handleClickCommit: function(e) {
        if (this.state.commitable) {
            this.props.commitItemCallback(this);
        }
    },

    text: function() {
        return this.refs.text.getDOMNode().value.trim();
    },

    url: function() {
        return this.refs.url.getDOMNode().value.trim();
    },

    render: function() {
        var textinput = React.createElement(
            'input',
            {ref: 'text',
             onKeyDown: this.handleKeyDownText,
             defaultValue: this.props.text
            }
        );

        var urlinput = React.createElement(
            'input',
            {ref: 'url',
             onKeyDown: this.handleKeyDownUrl,
             defaultValue: this.props.url
            }
        );

        var commitbutton = React.createElement(
            'button', {
                ref: 'commitbutton',
                disabled: !this.state.commitable,
                onClick: this.handleClickCommit
            },
            'done'
        );

        return React.createElement(
            'div', {className: 'linkedTextItemForEdit'},
            [textinput, urlinput, commitbutton]
        );
    }
});

/*
  One link that has been added.
  This should be able to let user to edit and delete the link.
*/
var LinkedTextListPreviewItem = React.createClass({
    getInitialState: function() {
        return {
            classSet: {'linkedTextListPreviewItem': true},
            editing: false,
            text: this.props.initialText,
            url: this.props.initialUrl
        };
    },

    removeItemCallback: function() {
        this.props.removeItemCallback(this.props.id);
    },

    editItemCallback: function() {
        this.setState({editing: true});
    },

    commitItemCallback: function(item) {
        this.setState({
            editing: false,
            text: item.text(),
            url: item.url(),
        });
    },

    addClass: function(name) {
        var classSet = this.state.classSet;
        classSet[name] = true;
        this.setState({classSet: classSet});
    },

    removeClass: function(name) {
        var classSet = this.state.classSet;
        delete classSet[name];
        this.setState(this.state.classSet);
    },

    handleDragStart: function(e) {
        e.dataTransfer.setData('text/plain', 'dummy');
        this.addClass('beingDragged');
    },

    handleDragEnter: function(e) {
        e.preventDefault();
        this.addClass('dragEntered');
    },

    handleDragOver: function(e) {
        e.preventDefault();
    },

    handleDragLeave: function(e) {
        this.removeClass('dragEntered');
    },

    handleDrop: function(e) {
        e.preventDefault();
        this.removeClass('dragEntered');
        return false;
    },

    handleDragend: function(e) {
        this.removeClass('beingDragged');
    },

    componentDidUpdate: function() {
        this.getDOMNode().addEventListener(
            'dragstart', this.handleDragStart, false);
        this.getDOMNode().addEventListener(
            'dragenter', this.handleDragEnter, false);
        this.getDOMNode().addEventListener(
            'dragover', this.handleDragOver, false);
        this.getDOMNode().addEventListener(
            'dragleave', this.handleDragLeave, false);
        this.getDOMNode().addEventListener(
            'drop', this.handleDrop, false);
        this.getDOMNode().addEventListener(
            'dragend', this.handleDragend, false);
    },

    render: function() {
        var itemForView = React.createElement(
            LinkedTextItemForView, {
                ref: 'view',
                text: this.state.text,
                url: this.state.url,
                removeItemCallback: this.removeItemCallback,
                editItemCallback: this.editItemCallback,
            }
        );

        var itemForEdit = React.createElement(
            LinkedTextItemForEdit, {
                ref: 'edit',
                text: this.state.text,
                url: this.state.url,
                commitItemCallback: this.commitItemCallback,
            }
        );

        return React.createElement(
            'li', {
                draggable: 'true',
                onDragOver: this.handleDragOver,
                onDragEnter: this.handleDragEnter,
                className: React.addons.classSet(this.state.classSet),
            }, this.state.editing ? itemForEdit : itemForView
        );
    }
});

/*
  List of linked text items that have been added.
  Intended for preview for user.
*/
var LinkedTextListPreview = React.createClass({
    getInitialState: function() {
        return {linklist: []};
    },

    removeItemCallback: function(id) {
        this.setState({
            linklist: this.state.linklist.filter((item) => {
                return item.id != id;
            })
        });
    },

    addItem: function(params) {
        params.id = new Date().getTime();
        this.setState({
            linklist: this.state.linklist.concat([params])
        });
    },

    render: function() {
        var items = this.state.linklist.map((item) => {
            return React.createElement(
                LinkedTextListPreviewItem, {
                    key: item.id,
                    id: item.id,
                    initialText: item.text,
                    initialUrl: item.url,
                    removeItemCallback: this.removeItemCallback
                }
            );
        });

        var list = React.createElement(
            'ul', {ref: 'list'}, items
        );

        return React.createElement(
            'div', {
                className: 'linkedTextListPreview',
            }, [list]
        );
    }
});

/*
  Component that lets you create list of links.
*/
var ReferenceLinkLists　= React.createClass({
    getInitialState: function() {
        return {linklist: []};
    },

    addItemCallback: function() {
        var adder = this.refs.adder;
        var text = adder.refs.text.getDOMNode().value.trim();
        var url = adder.refs.url.getDOMNode().value.trim();
        if (!url) {
            return;
        }
        if (!text) {
            text = url;
        }

        this.refs.preview.addItem({text: text, url: url});

        adder.refs.text.getDOMNode().value = '';
        adder.refs.url.getDOMNode().value='';
        adder.refs.text.getDOMNode().focus();
        return;
    },

    render: function() {
        var caption = React.createElement(
            'h3', {ref: 'caption'}, this.props.caption
        );

        var linkedTextItemAdder = React.createElement(
            LinkedTextItemAdder, {
                ref: 'adder',
                addItemCallback: this.addItemCallback
            }
        );

        var linkListPreview = React.createElement(
            LinkedTextListPreview, {
                ref: 'preview',
            }
        );

        return React.createElement(
            'div', {className: 'showNotes'},
            [caption, linkedTextItemAdder, linkListPreview]
        );
    }
});

var EpisodeDetail = React.createClass({
    render: function() {
        var title = React.createElement(
            TextInput,
            {caption: 'Title', placeholder: ''}
        );

        var description = React.createElement(
            CharacterCountRestrictionTextarea,
            {caption: 'Description',
             placeholder: 'Enter here...',
             maxcount: 255}
        );

        var shownotes = React.createElement(
            ReferenceLinkLists,
            {caption: 'Show Notes'}
        );

        return React.createElement(
            'div', {className: 'episodeDetail'},
            [title, description, shownotes]
        );
    }

});


// Episode entry
React.render(
    React.createElement(
        EpisodeDetail
    ),
    document.getElementById('content')
);
