import { Component, type ReactNode } from 'react';

/** Replaces a blank page with a way back if anything ever throws while rendering. */
export class ErrorBoundary extends Component<{ children: ReactNode }, { error: string | null }> {
  state = { error: null as string | null };

  static getDerivedStateFromError(error: unknown) {
    return { error: error instanceof Error ? error.message : String(error) };
  }

  componentDidCatch(error: unknown) {
    console.error(error);
  }

  private restart = () => {
    try {
      localStorage.removeItem('wk.settings');
    } catch {
      // Storage unavailable; reloading is still worth a try.
    }
    location.reload();
  };

  render() {
    if (this.state.error == null) return this.props.children;
    return (
      <main className="screen center-screen">
        <h1>صار في خلل بسيط 😅</h1>
        <p className="muted">اكبس الزر وارجع للعب. إذا تكرر، ابعتلنا صورة للرسالة تحت.</p>
        <button className="btn btn--primary btn--xl" onClick={this.restart}>
          ابدأ من جديد
        </button>
        <code className="error-detail" dir="ltr">
          {this.state.error}
        </code>
      </main>
    );
  }
}
