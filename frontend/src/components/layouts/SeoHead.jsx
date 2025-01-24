import { Helmet, HelmetData } from "react-helmet-async";

const helmetData = new HelmetData({});

const SeoHead = ({ title = "", description = "" }) => {
  return (
    <Helmet
      helmetData={helmetData}
      title={title ? title : undefined}
      defaultTitle="CSAM AI"
    >
      <meta name="description" content={description} />
    </Helmet>
  );
};

export default SeoHead;
