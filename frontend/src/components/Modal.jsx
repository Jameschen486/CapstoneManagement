// Modal.jsx for modal boxes when we press notification or messages
import React from 'react';
import '../css/Modal.css';

const Modal = ({ show, handleClose, title, children }) => {
  const showHideClassName = show ? "modal display-block" : "modal display-none";

  return (
    <div className={showHideClassName}>
      <section className="modal-main">
        <h2>{title}</h2>
        {children}
        <button type="button" onClick={handleClose}>
          Close
        </button>
      </section>
    </div>
  );
};

export default Modal;
