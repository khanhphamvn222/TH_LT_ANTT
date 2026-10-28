import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function Home() {
  return (
    <Layout
      title="Báo cáo Thực hành DevSecOps"
      description="Bài thực hành 6: Bảo mật với DevSecOps - Phạm Duy Khánh">
      <main style={{ padding: '4rem 2rem', textAlign: 'center' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>
          Bài 6: Bảo mật với DevSecOps
        </h1>
        <p style={{ fontSize: '1.25rem', color: '#555' }}>
          Sinh viên thực hiện: <strong>Phạm Duy Khánh</strong> | MSSV: <strong>2387700029</strong>
        </p>
        <p style={{ maxWidth: '600px', margin: '1.5rem auto', lineHeight: '1.6' }}>
          Trang web tài liệu được tự động xây dựng (Build), đóng gói (Artifacts) và triển khai (Deploy)
          thông qua hệ thống CI/CD Pipeline tự động hóa.
        </p>
        <div style={{ marginTop: '2rem' }}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Xem Tài liệu Thực hành 🚀
          </Link>
        </div>
      </main>
    </Layout>
  );
}
