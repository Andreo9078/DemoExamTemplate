import React from "react";
import {
  Button,
  Radio,
  Space,
  Tooltip,
} from "antd";
import {
  DownloadOutlined,
  SearchOutlined,
  DeleteOutlined,
  PlusOutlined,
} from "@ant-design/icons";

export const ButtonGallery: React.FC = () => {
  return (
      <Space direction="vertical" size="large" style={{width: "100%"}}>
        <h1>Кнопки</h1>
        {/* Типы кнопок */}
        <div>
          <h3>Типы</h3>
          <Space>
            <Button type="primary">Primary</Button>
            <Button>Default</Button>
            <Button type="dashed">Dashed</Button>
            <Button type="text">Text</Button>
            <Button type="link">Link</Button>
          </Space>
        </div>

        {/* Размеры */}
        <div>
          <h3>Размеры</h3>
          <Space>
            <Button type="primary" size="large">
              Large
            </Button>
            <Button type="primary" size="middle">
              Middle
            </Button>
            <Button type="primary" size="small">
              Small
            </Button>
          </Space>
        </div>

        {/* Иконки */}
        <div>
          <h3>С иконками</h3>
          <Space>
            <Button icon={<SearchOutlined/>}>Search</Button>
            <Button icon={<DownloadOutlined/>}>Download</Button>
            <Button icon={<DeleteOutlined/>} danger>
              Delete
            </Button>
            <Button shape="circle" icon={<PlusOutlined/>}/>
            <Button shape="round" icon={<PlusOutlined/>}>
              Add
            </Button>
          </Space>
        </div>

        {/* Загрузка */}
        <div>
          <h3>Загрузка</h3>
          <Space>
            <Button type="primary" loading>
              Loading
            </Button>
            <Button type="primary" loading icon={<DownloadOutlined/>}>
              Loading
            </Button>
            <Button loading/>
          </Space>
        </div>

        {/* Disabled */}
        <div>
          <h3>Отключенные</h3>
          <Space>
            <Button type="primary" disabled>
              Primary
            </Button>
            <Button disabled>Default</Button>
            <Button type="dashed" disabled>
              Dashed
            </Button>
            <Button type="text" disabled>
              Text
            </Button>
            <Button type="link" disabled>
              Link
            </Button>
          </Space>
        </div>

        {/* Danger */}
        <div>
          <h3>Опасные (Danger)</h3>
          <Space>
            <Button danger>Default</Button>
            <Button type="primary" danger>
              Primary
            </Button>
            <Button type="dashed" danger>
              Dashed
            </Button>
            <Button type="text" danger>
              Text
            </Button>
            <Button type="link" danger>
              Link
            </Button>
          </Space>
        </div>

        {/* Ghost (на цветном фоне) */}
        <div style={{background: "#000", padding: 16}}>
          <h3 style={{color: "#fff"}}>Ghost (на цветном фоне)</h3>
          <Space>
            <Button type="primary" ghost>
              Primary
            </Button>
            <Button ghost>Default</Button>
            <Button type="dashed" ghost>
              Dashed
            </Button>
          </Space>
        </div>

        {/* Tooltip */}
        <div>
          <h3>С подсказкой (Tooltip)</h3>
          <Space>
            <Tooltip title="Скачать файл">
              <Button icon={<DownloadOutlined/>}/>
            </Tooltip>
            <Tooltip title="Удалить">
              <Button icon={<DeleteOutlined/>} danger/>
            </Tooltip>
          </Space>
        </div>

        <div>
          <h3>Radio.Group</h3>
          <Radio.Group>
            <Radio.Button value="large">Large</Radio.Button>
            <Radio.Button value="default">Default</Radio.Button>
            <Radio.Button value="small">Small</Radio.Button>
          </Radio.Group>
        </div>
      </Space>

  );
};

export default ButtonGallery;
