import React, { Component, PropTypes } from 'react'
import { Tooltip, Icon } from 'antd'

// export default function overrideTable(ComposedComponent) {
//   class NewComponent extends Component {
//     constructor() {
//       super(...arguments);
//       this.state = { columns: [] };
//     }
//     componentDidMount() {
//       var self = this;
//       let oldColumns = this.props.columns;
//       let newColumns = oldColumns;
//       oldColumns.forEach((columnValue, columnIndex) => {
//         // let originRender = columnValue.render || function(){};
//         // newColumns[columnIndex].render = (item, record, dataIndex) => {
//         //   return (
//         //     <div className="column-box-wrapper">{originRender(item, record, dataIndex)}</div>
//         //   );
//         // }
//         props.columns[columnIndex].title = (
//           <Tooltip placement="topLeft" title={
//             <span style={{cursor: 'pointer'}} onClick={self.removeOneColumn.bind(self)}>关闭此栏</span>
//           }>
//             <div>{columnValue.title}</div>
//           </Tooltip>
//         )
//       });
//     }
//     render() {
//       return <ComposedComponent {...this.props} data={this.state.data} />;
//     }
//   }
//   NewComponent.propTypes = {
//     // whatever
//   };
//   return NewComponent;
// }



export function tableDecoratorAddColumnCloseButton(ComposedComponent){
  class AlchemistTableEnhancer extends ComposedComponent {
    constructor() {
      super(...arguments);

      this.state = this.state || {};
      this.deletedColumnIndexes = [];
    }

    removeOneColumn(targetColumnValue) {
      this.deletedColumnIndexes.push(targetColumnValue['index']);
    }

    syncToLimitedColumns(props) {
      var self = this;
      self.deletedColumnIndexes.forEach((deletedIndex) => {
        props.columns.forEach((columnValue, columnIndex) => {
          if (deletedIndex == columnValue['index']) {
            props.columns.splice(columnIndex, 1);
          }
        })
      });
      this.forceUpdate()
    }

    componentWillReceiveProps(props) {
      var self = this;
      this.syncToLimitedColumns(props);

      props.columns.forEach((columnValue, columnIndex) => {
        props.columns[columnIndex].title = (
          <Tooltip placement="topLeft" title={
            <span style={{cursor: 'pointer'}} onClick={() => {self.removeOneColumn(columnValue); self.syncToLimitedColumns(props);}}>关闭此列</span>
          }>
            <span>{columnValue.title}</span>
          </Tooltip>
        );
      });

      // props.columns = newColumns;

      if (super.componentWillReceiveProps) {
        super.componentWillReceiveProps(props);
      }
    }

    componentWillUnmount() {
      if (super.componentWillUnmount) {
        super.componentWillUnmount();
      }

    }

    render() {
      const renderedElement = super.render();
      return renderedElement;
    }
  }

  return AlchemistTableEnhancer;
}

export function tableDecoratorAddColumnWidthAlter(ComposedComponent){
  class AlchemistTableEnhancer extends ComposedComponent {
    constructor() {
      super(...arguments);

      this.state = this.state || {};
      // this.columnWidths = [];
    }

    // removeOneColumn(targetColumnValue) {
    //   this.deletedColumnIndexes.push(targetColumnValue['index']);
    // }
    //
    // syncToColumns(props) {
    //   var self = this;
    //   self.deletedColumnIndexes.forEach((deletedIndex) => {
    //     props.columns.forEach((columnValue, columnIndex) => {
    //       if (deletedIndex == columnValue['index']) {
    //         props.columns.splice(columnIndex, 1);
    //       }
    //     })
    //   });
    //   this.forceUpdate()
    // }

    componentWillReceiveProps(props) {
      var self = this;
      // this.syncToLimitedColumns(props);
      //
      // props.columns.forEach((columnValue, columnIndex) => {
      //   props.columns[columnIndex].title = (
      //     <span>
      //       <span>{columnValue.title}</span>
      //       {" "}
      //       <Icon style={{cursor: 'move'}} type="shrink" id={"table-column-resize-btn-"+columnIndex} />
      //     </span>
      //   );
      // });

      // props.columns = newColumns;

      if (super.componentWillReceiveProps) {
        super.componentWillReceiveProps(props);
      }
    }

    componentWillUnmount() {
      if (super.componentWillUnmount) {
        super.componentWillUnmount();
      }

    }

    render() {
      const renderedElement = super.render();
      return renderedElement;
    }
  }

  return AlchemistTableEnhancer;
}
