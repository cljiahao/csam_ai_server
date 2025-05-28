const Placeholder = ({ text }) => {
  return (
    <div className="h-5/6 w-11/12 rounded-xl border-4 border-dashed border-gray-400 bg-gray-100">
      <p className="flex-center hw-full text-bold text-5xl text-red-500">
        {text}
      </p>
    </div>
  );
};

export default Placeholder;
