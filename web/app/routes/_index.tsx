import type { MetaFunction } from "@remix-run/node";

export const meta: MetaFunction = () => {
  return [
    { title: "UK Goverment Contact List" },
    { name: "description", content: "UK Goverment Contact List" },
  ];
};

export default function Index() {
  return (
    <div className="container mx-auto my-10 px-4 grid md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-4">
      <div className="card bg-base-100 shadow-md">
        <figure>
          <img
            src="https://img.daisyui.com/images/stock/photo-1606107557195-0e29a4b5b4aa.webp"
            alt="Shoes"
          />
        </figure>
        <div className="card-body">
          <h1 className="card-title font-bold text-2xl">Hello World</h1>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam,
            quos.
          </p>
          <div className="card-actions mt-2">
            <button className="btn btn-primary">Click me</button>
          </div>
        </div>
      </div>
    </div>
  );
}
